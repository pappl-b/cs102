#! /usr/bin/env python3

import argparse
import pathlib
from typing import Any, Dict, Union

from life import GameOfLife
from life_console import Console


def arg_parser() -> Dict[str, Any]:
    """
    Собирает аргументы командной строки в словарь

    Returns Dict[str, Any]:
        rows (int): количество строк
        cols (int): количество столбцов
        rand (bool): рандомное ли поле
        max_gen (float): максимальное количество поколений
        from_file (Optional[pathlib.Path]): путь к файлу из которого начнется игра
        save_path (pathlib.Path): путь к файлу, в который сохранится игра
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--rows", "-r", type=int, default=20, help="Количество строк")
    argument_parser.add_argument("--cols", "-c", type=int, default=20, help="Количество столбцов")
    argument_parser.add_argument(
        "--rand", action="store_true", default=False, help="Рандомное ли поле"
    )
    argument_parser.add_argument(
        "--max_gen",
        type=float,
        default=float("inf"),
        help="Максимальное количество поколений",
    )
    argument_parser.add_argument(
        "--from_file",
        "-f",
        type=str,
        default="",
        help="Путь к файлу из которого начнется игра",
    )
    argument_parser.add_argument(
        "--save_path",
        type=pathlib.Path,
        default=pathlib.Path("grid"),
        help="Путь к файлу сохранения",
    )
    return vars(argument_parser.parse_args())


def main():
    args = arg_parser()
    if args["from_file"] != "":
        life = GameOfLife.from_file(pathlib.Path(args["from_file"]))
    else:
        life = GameOfLife(
            size=(args["rows"], args["cols"]),
            randomize=args["rand"],
            max_generations=args["max_gen"],
        )
    console = Console(life, save_path=args["save_path"])
    console.run()


if __name__ == "__main__":
    main()
