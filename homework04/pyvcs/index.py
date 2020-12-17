import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        head = struct.pack(
            "!LLLLLLLLLL20sH",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
        )
        name_bytes = self.name.encode()
        return head + name_bytes + b"\x00" * (8 - (62 + len(name_bytes)) % 8)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        head = struct.unpack("!LLLLLLLLLL20sH", data[:62])
        name_bytes = data[62:]
        name_bytes = name_bytes[: name_bytes.find(b"\x00")]
        return GitIndexEntry(
            ctime_s=head[0],
            ctime_n=head[1],
            mtime_s=head[2],
            mtime_n=head[3],
            dev=head[4],
            ino=head[5] & 0xFFFFFFFF,
            mode=head[6],
            uid=head[7],
            gid=head[8],
            size=head[9],
            sha1=head[10],
            flags=head[11],
            name=name_bytes.decode("ascii"),
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not pathlib.Path(gitdir / "index").exists():
        return []
    index_file = open(pathlib.Path(gitdir / "index"), "rb")
    content = index_file.read()

    signature = content[:4].decode("ascii")
    version = content[4:8].decode("ascii")
    files_count = struct.unpack("!L", content[8:12])[0]

    returning: tp.List[GitIndexEntry] = []

    content = content[12:]

    for _ in range(files_count):
        gie = GitIndexEntry.unpack(content)
        bound = content.find(gie.name.encode()) + len(gie.name)
        content = content[bound:]

        while content[0] == 0:
            content = content[1:]

        returning.append(gie)

    return returning


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    signature = b"DIRC"
    version = 2
    result_index = struct.pack("!4sLL", signature, version, len(entries))
    for gie in entries:
        result_index += gie.pack()
    f = open(str(gitdir / "index"), "wb")
    f.write(result_index + hashlib.sha1(result_index).digest())
    f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    list_gie = read_index(gitdir)
    if details:
        for gie in list_gie:
            print(" ".join([str(f"{gie.mode:o}"), gie.sha1.hex(), str(0)]) + "\t" + gie.name)
    else:
        for gie in list_gie:
            print(gie.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    index_path = pathlib.Path(gitdir / "index")
    gie_list_new: tp.List[GitIndexEntry] = []
    names = []
    if os.path.exists(index_path):
        gie_list_new = read_index(gitdir)
        for elem in gie_list_new:
            names.append(elem.name)
    for route in paths:
        stats = os.stat(route)

        ctimes = str(stats.st_ctime).split(".")
        mtimes = str(stats.st_mtime).split(".")

        gie_to_append = GitIndexEntry(
            ctime_s=int(ctimes[0]),
            ctime_n=int(ctimes[1]),
            mtime_s=int(mtimes[0]),
            mtime_n=int(mtimes[1]),
            dev=stats.st_dev,
            ino=stats.st_ino & 0xFFFFFFFF,
            mode=stats.st_mode,
            uid=stats.st_uid,
            gid=stats.st_gid,
            size=stats.st_size,
            sha1=bytes.fromhex(hash_object(route.read_bytes(), "blob", True)),
            flags=0,
            name=str(route),
        )
        if names.count(str(route)):
            gie_list_new[names.index(str(route))] = gie_to_append
        else:
            gie_list_new.append(gie_to_append)
    gie_list_new.sort(key=lambda GitIndexEntry: GitIndexEntry.name)
    write_index(gitdir, gie_list_new)
