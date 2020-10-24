from random import randint
from typing import List, Optional, Set, Tuple, TypeVar


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


T = TypeVar("T")


def group(values: List[T], n: int) -> List[List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[row * n : (row + 1) * n] for row in range(n)]


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [item[pos[1]] for item in grid]


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    upleft_i = pos[0] // 3 * 3
    upleft_j = pos[1] // 3 * 3
    for i in range(3):
        for j in range(3):
            block.append(grid[upleft_i + i][upleft_j + j])
    return block


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    empty_row = 0
    empty_col = 0

    for row in grid:
        empty_col = 0
        for elem in row:
            if elem == ".":
                return (empty_row, empty_col)
            empty_col += 1
        empty_row += 1
    return None


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row = set(get_row(grid, pos))
    col = set(get_col(grid, pos))
    block = set(get_block(grid, pos))
    possible = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

    return possible.difference(row, col, block)


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos == None:
        return grid
    else:
        values = find_possible_values(grid, pos)
        if len(values) == 0:
            return grid
        for value in values:
            grid[pos[0]][pos[1]] = value
            newgrid = solve(grid)
            if sum(1 for row in grid for e in row if e == ".") > 0:
                grid[pos[0]][pos[1]] = "."
            else:
                return newgrid
        return grid


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(9):
        currpos = (i, (i * 3) % 9 + (i * 3) // 9)
        if not (
            set(get_row(solution, currpos))
            == set(get_col(solution, currpos))
            == set(get_block(solution, currpos))
            == {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        ):
            return False
    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    sudoku = [[str((i + j * 3 + j // 3) % 9 + 1) for i in range(9)] for j in range(9)]
    sudoku = ([list(row) for row in zip(*sudoku)]).copy()
    repeat = randint(50, 70)

    for i in range(repeat):
        sudoku = ([list(row) for row in zip(*sudoku)]).copy()
        row1_index = randint(0, 8)
        row2_index = row1_index // 3 * 3 + randint(0, 2)
        row_remember = sudoku[row1_index].copy()
        sudoku[row1_index] = sudoku[row2_index].copy()
        sudoku[row2_index] = row_remember.copy()

    for i in range(repeat):
        sudoku = ([list(row) for row in zip(*sudoku)]).copy()
        row1_index = randint(0, 2)
        row2_index = (row1_index + 1) % 3 * 3
        row1_index *= 3
        for j in range(3):
            row_remember = sudoku[row1_index + j].copy()
            sudoku[row1_index + j] = sudoku[row2_index + j].copy()
            sudoku[row2_index + j] = row_remember.copy()

    for i in range(81 - N):
        is_removed = False
        while not is_removed:
            indx = randint(0, 80)
            row = indx // 9
            col = indx % 9
            if sudoku[row][col] != ".":
                sudoku[row][col] = "."
                is_removed = True

    return sudoku


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)