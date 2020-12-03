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
    return hashlib.sha1(store).hexdigest()


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not (3 < len(obj_name) < 41):
        raise Exception("Not a valid object name " + obj_name)

    contents = []

    dir_name = obj_name[:2]
    file_starts_with = obj_name[2:]

    files_in_dir = os.listdir(pathlib.Path(gitdir / "objects" / dir_name))

    for fl in files_in_dir:
        if fl.startswith(file_starts_with):
            obj_path = pathlib.Path(gitdir / "objects" / obj_name[:2] / fl)
            contents.append(obj_name[:2] + fl)
            # obj_content_bytes = obj_path.read_bytes()
            # raise Exception(obj_content_bytes)
            # obj_data = zlib.decompress(obj_content_bytes)
            # header_separator = obj_data.find(b"\x00")
            # len_separator = obj_data[:header_separator].find(b" ")

            # content_len = int(obj_data[len_separator:header_separator].decode("ascii"))
            # contents.append(str(obj_data[header_separator+1:]))
    if len(contents) == 0:
        raise Exception("Not a valid object name " + obj_name)

    return contents


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
