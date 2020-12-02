import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    if workdir == (pathlib.Path(".")).absolute():
        return pathlib.Path(workdir / os.environ["GIT_DIR"])
    found_repo = ""
    is_first = True
    for elem in workdir.parts:
        found_repo += elem

        if elem == os.environ["GIT_DIR"]:
            return pathlib.Path(found_repo)

        if is_first:
            is_first = False
        else:
            found_repo += "/"

    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)

    if not pathlib.Path.is_dir(workdir):
        raise Exception(f"{workdir} is not a directory")
    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"

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
