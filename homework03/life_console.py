import curses
import pathlib
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, speed: int = 1, path_saving: str = "grid") -> None:
        super().__init__(life)
        # Скорость протекания игры
        self.speed = speed
        # Сохранение игры
        self.path_saving = pathlib.Path(path_saving)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """
        Отрисовка списка клеток.
        """
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col]:
                    screen.addstr(row+1, col*2+1, "  ", curses.A_REVERSE)
                else:
                    screen.addstr(row+1, col*2+1, "  ")

    def run(self) -> None:
        screen = curses.initscr()
        screen = curses.newwin(self.life.rows + 2, self.life.cols*2 + 2)
        screen.keypad(True)
        curses.noecho()
        curses.curs_set(0)
        screen.border(0)
        screen.nodelay(True)
        
        
        self.draw_borders(screen)

        running = True
        paused = False

        while running:
            key = screen.getch()
            if key == ord(' '):
                paused = bool((int(paused)+1)%2)
            elif key == curses.KEY_RIGHT:   
                self.life.save(self.path_saving)
            elif key == curses.KEY_LEFT:   
                self.life.curr_generation = self.life.create_grid(True)
            if not paused:
                self.draw_grid(screen)
                screen.refresh()
                self.life.step()
                time.sleep(self.speed)
        curses.endwin()
