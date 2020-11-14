""" User Interface in Console """
import pathlib
import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    """ Interface to play 'Game of Life' in the window """

    def __init__(
        self, life: GameOfLife, cell_size: int = 10, speed: int = 10, path_saving: str = "grid"
    ) -> None:
        super().__init__(life)
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed

        # Сохранение игры
        self.path_saving = pathlib.Path(path_saving)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        [
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ],
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        [
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ],
                    )

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = bool((int(paused) + 1) % 2)
                    if event.key == pygame.K_s:
                        self.life.save(self.path_saving)
                    if event.key == pygame.K_r:
                        self.life.curr_generation = self.life.create_grid(randomize=True)
                        self.life.generations = 1
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()
                if paused and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos_y, pos_x = pygame.mouse.get_pos()
                    pos_x = pos_x // self.cell_size
                    pos_y = pos_y // self.cell_size
                    self.life.curr_generation[pos_x][pos_y] = (
                        self.life.curr_generation[pos_x][pos_y] + 1
                    ) % 2
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()

            if not paused:
                self.life.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()

            clock.tick(self.speed)
        pygame.quit()
