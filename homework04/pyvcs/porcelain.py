import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    for path in paths:
        if path.is_dir():
            add(gitdir, list(path.glob("*")))
        else:
            update_index(gitdir, [path])


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    gie_list = read_index(gitdir)
    tree = write_tree(gitdir, gie_list)
    commit_msg = commit_tree(gitdir, tree, message, resolve_head(gitdir), author)
    update_ref(gitdir, get_ref(gitdir), commit_msg)
    return commit_msg


def create_tree_content(gitdir: pathlib.Path, tree_sha: bytes, dirname: str = ""):
    content = read_tree(tree_sha)
    for item in content:
        file_route = dirname + "/" + item[2]
        if item[0] == 40000:
            os.mkdir(file_route)
            create_tree_content(gitdir, item[1].encode(), file_route)
        else:
            create_file = open(file_route, "wb")
            create_file.write(read_object(item[1], gitdir)[1])
            create_file.close()
            pathlib.Path.chmod(pathlib.Path(file_route), int(str(item[0]), 8))


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    fmt, content = read_object(obj_name, gitdir)
    if fmt != "commit":
        raise Exception("Not a suitable object type")
    for row in read_index(gitdir):
        if pathlib.Path(row.name).exists():
            os.remove(pathlib.Path(row.name))
            dir_content = os.listdir(pathlib.Path(row.name).parent)
            if not dir_content:
                os.removedirs(pathlib.Path(row.name).parent)
    create_tree_content(gitdir, commit_parse(content).encode())
