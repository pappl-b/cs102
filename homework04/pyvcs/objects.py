import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    hashed = hashlib.sha1(store).hexdigest()
    if write:
        current_dir = repo_find(pathlib.Path.cwd()) / "objects" / pathlib.Path(hashed[:2])
        if not pathlib.Path.exists(current_dir):
            pathlib.Path.mkdir(current_dir)
        file_obj = pathlib.Path(current_dir / hashed[2:])
        file_obj.write_bytes(zlib.compress(store))
    return hashed


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not (3 < len(obj_name) < 41):
        raise Exception("Not a valid object name " + obj_name)

    contents = []

    dir_name = obj_name[:2]
    file_starts_with = obj_name[2:]

    files_in_dir = os.listdir(pathlib.Path(gitdir / "objects" / dir_name))

    for fl in files_in_dir:
        if fl.startswith(file_starts_with):
            # obj_path = pathlib.Path(gitdir / "objects" / obj_name[:2] / fl)
            contents.append(obj_name[:2] + fl)
    if len(contents) == 0:
        raise Exception("Not a valid object name " + obj_name)

    return contents


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    obj_bytes = pathlib.Path(gitdir / "objects" / sha[:2] / sha[2:]).read_bytes()
    obj_data = zlib.decompress(obj_bytes)

    header_separator = obj_data.find(b"\x00")
    len_separator = obj_data[:header_separator].find(b" ")

    content_len = int(obj_data[len_separator:header_separator].decode("ascii"))

    content = obj_data[header_separator + 1 :]

    if len(content) != content_len:
        raise Exception("The file is corrupted")

    fmt = obj_data[:len_separator].decode("ascii")

    return (fmt, content)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    gitdir = repo_find(pathlib.Path.cwd())
    bytes_in_tree = pathlib.Path(
        gitdir / "objects" / data[:2].decode("ascii") / data[2:].decode("ascii")
    ).read_bytes()
    data_in_tree = zlib.decompress(bytes_in_tree)

    content_list: tp.List[tp.Tuple[int, str, str]] = []

    header_separator = data_in_tree.find(b"\x00")
    len_separator = data_in_tree[:header_separator].find(b" ")
    content_len = int(data_in_tree[len_separator:header_separator])

    content = data_in_tree[header_separator + 1 :]

    while content_len > 10:
        separator = content.find(b" ")
        content_len -= separator
        row_mode = content[:separator].decode()

        content = content[separator + 1 :]

        separator = content.find("\0".encode())
        row_name = content[:separator]
        row_sha = content[separator + 1 : separator + 21]
        content = content[separator + 21 :]
        content_len -= separator + 20
        content_list.append((int(row_mode), row_sha.hex(), row_name.decode()))

    return content_list


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(pathlib.Path.cwd())
    fmt, content = read_object(obj_name, pathlib.Path(gitdir))
    if fmt != "tree":
        gitdir = repo_find(pathlib.Path.cwd())
        fmt, content = read_object(obj_name, pathlib.Path(gitdir))
        to_print = content.decode("ascii")
        print(to_print)
    else:
        tree_content = read_tree(obj_name.encode())
        for part in tree_content:
            row = ""
            if part[0] == 40000:
                row += "040000 "
            else:
                row += str(part[0]) + " "
            fmt, content = read_object(part[1], pathlib.Path(gitdir))
            row += fmt + " " + part[1] + "\t" + part[2]
            print(row)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
