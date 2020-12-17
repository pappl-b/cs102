import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    found_repo = pathlib.Path(workdir).absolute()
    root = pathlib.Path(found_repo.parts[0])

    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"

    while True:
        if os.listdir(found_repo).count(os.environ["GIT_DIR"]) == 1:
            return pathlib.Path(found_repo / os.environ["GIT_DIR"]).absolute()
        found_repo = found_repo.parent
        if found_repo == root:
            break

    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)

    if not pathlib.Path.is_dir(workdir):
        raise Exception(f"{workdir} is not a directory")
    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"
    if os.getenv("GIT_AUTHOR_NAME") is None:
        if os.getenv("USERNAME") is None:
            os.environ["USERNAME"] = "spasisohrani"
        os.environ["GIT_AUTHOR_NAME"] = os.environ["USERNAME"]
        os.environ["GIT_AUTHOR_EMAIL"] = "not@stated"

    pathlib.Path.mkdir(pathlib.Path(workdir) / os.environ["GIT_DIR"])

    rootrepo = pathlib.Path(workdir) / os.environ["GIT_DIR"]

    pathlib.Path.mkdir(rootrepo / "refs")
    pathlib.Path.mkdir(rootrepo / "refs" / "heads")
    pathlib.Path.mkdir(rootrepo / "refs" / "tags")
    pathlib.Path.mkdir(rootrepo / "objects")

    head = pathlib.Path(rootrepo / "HEAD")
    head.write_text("ref: refs/heads/master\n")

    config = pathlib.Path(rootrepo / "config")
    config.write_text(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
    )

    description = pathlib.Path(rootrepo / "description")
    description.write_text("Unnamed pyvcs repository.\n")

    return rootrepo
