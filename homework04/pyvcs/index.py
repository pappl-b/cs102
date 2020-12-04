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
            "!10L20sH",
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
        return head + name_bytes + b"\x00" * (len(name_bytes) % 4)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        head = struct.unpack("!10L20sH", data[:62])
        name_bytes = data[62:]
        name_bytes = name_bytes[: name_bytes.find(b"\x00")]

        return GitIndexEntry(
            ctime_s=head[0],
            ctime_n=head[1],
            mtime_s=head[2],
            mtime_n=head[3],
            dev=head[4],
            ino=head[5],
            mode=head[6],
            uid=head[7],
            gid=head[8],
            size=head[9],
            sha1=head[10],
            flags=head[11],
            name=name_bytes.decode(),
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not pathlib.Path(gitdir / "index").exists():
        return []
    index_file = open(pathlib.Path(gitdir / "index"), "rb")
    content = index_file.read()

    signature = content[:4].decode()
    version = content[4:8].decode()
    files_count = struct.unpack("!L", content[8:12])[0]

    returning: tp.List[GitIndexEntry] = []

    content = content[12:]

    for _ in range(files_count):
        gie = GitIndexEntry.unpack(content)
        bound = content.find(gie.name.encode()) + len(gie.name)
        content = content[bound:]

        incycle = []
        while content[0] == 0:
            incycle.append(content[0])
            content = content[1:]

        returning.append(gie)

    return returning


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
