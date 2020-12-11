import os
import pathlib
import stat
import time
import typing as tp

import hashlib

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_entries : tp.List[bytes] = []
    for gie in index:
        
        row = str(f"{gie.mode:o}") + " " + gie.name + "\0"
        tree_entries.append(row.encode() + gie.sha1)

    all_objects = b""
    for entry in tree_entries:
        all_objects += entry

    return hash_object(all_objects, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
