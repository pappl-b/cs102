import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    ref_path = pathlib.Path(gitdir / pathlib.Path(ref))
    new_ref = open(ref_path, "w")
    new_ref.write(new_value)
    new_ref.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    ref = pathlib.Path(pathlib.Path(gitdir.absolute() / pathlib.Path(refname)))
    ref_content = ref.read_text()
    return ref_content


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    ref_path: pathlib.Path
    if is_detached(gitdir):
        ref_path = pathlib.Path(gitdir / "HEAD")
    else:
        ref_path = pathlib.Path(gitdir / pathlib.Path(get_ref(gitdir)))
        if not ref_path.exists():
            return None

    return ref_path.read_text()


def is_detached(gitdir: pathlib.Path) -> bool:
    head = pathlib.Path(gitdir / "HEAD")
    content = head.read_text()
    if content.find("ref: ") == -1:
        return True
    else:
        return False


def get_ref(gitdir: pathlib.Path) -> str:
    in_head = pathlib.Path(gitdir / "HEAD").read_text()
    sepataror = in_head.find("ref: ")
    content = in_head[sepataror + 5 :]
    content = content[: content.find("\n")]
    return content
