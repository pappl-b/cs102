"""
Logic for 'Game of Life'
"""
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """ Game proccess realisation """

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [
                [(random.randint(0, 1)) for col in range(self.cols)] for row in range(self.rows)
            ]
        return [[0] * self.cols for i in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        row, col = cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                current_row = row + i
                current_col = col + j
                if (-1 < current_row < self.rows) and (-1 < current_col < self.cols):
                    neighbours.append(self.curr_generation[current_row][current_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid(randomize=False)
        for row in range(self.rows):
            for col in range(self.cols):
                new_grid[row][col] = sum(self.get_neighbours((row, col)))

        for row in range(self.rows):
            for col in range(self.cols):
                if self.curr_generation[row][col]:
                    if 1 < new_grid[row][col] < 4:
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0
                else:
                    if new_grid[row][col] == 3:
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation = self.curr_generation.copy()
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file_from = open(filename)
        importing_grid: Grid
        importing_grid = []
        importing_height = 0

        for line in file_from:
            importing_grid.append([])
            for elem in line.strip("\n"):
                importing_grid[importing_height].append(int(elem))
            importing_height += 1

        importing_game = GameOfLife((importing_height, len(importing_grid[0])))
        importing_game.curr_generation = importing_grid
        return importing_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file_to = open(filename, "w")
        for row in self.curr_generation:
            for col in row:
                file_to.write(str(col))
            file_to.write("\n")
        file_to.close()
