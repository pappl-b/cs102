import hashlib
import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def gie_from_list_in_dir(gie_list: tp.List[GitIndexEntry], dirname: str) -> tp.List[GitIndexEntry]:
    gies_in_dir: tp.List[GitIndexEntry] = []
    for gie in gie_list:
        if gie.name.find(dirname) == 0:
            gies_in_dir.append(gie)
    return gies_in_dir


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_entries = b""
    for gie in index:
        current_place = gie.name[len(dirname) :]
        name_parts = current_place.split("/")
        if len(name_parts) != 1:
            new_dirname = dirname + name_parts[0] + "/"
            row = "40000 " + name_parts[0] + "\0"
            dir_sha = write_tree(
                gitdir, gie_from_list_in_dir(index, new_dirname), dirname=new_dirname
            )
            tree_entries += row.encode() + bytes.fromhex(dir_sha)
        else:
            row = str(f"{gie.mode:o}") + " " + name_parts[0] + "\0"
            tree_entries += row.encode() + gie.sha1
    return hash_object(tree_entries, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:

    commiter = os.environ["GIT_AUTHOR_NAME"] + " <" + os.environ["GIT_AUTHOR_EMAIL"] + ">"
    if author is None:
        author = commiter

    string_to_commit = "tree " + tree + "\n"
    string_to_commit += (
        "author " + author + " " + str(int(time.mktime(time.localtime()))) + " +0300\n"
    )
    string_to_commit += (
        "committer " + author + " " + str(int(time.mktime(time.localtime()))) + " +0300\n\n"
    )
    string_to_commit += message + "\n"

    return hash_object(string_to_commit.encode(), "commit", write=True)
