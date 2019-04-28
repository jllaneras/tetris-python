import curses
import time

from tetrimino import Tetrimino
from constants import (
    MATRIX_WIDTH,
    MATRIX_HEIGHT,
    MATRIX_POS,
    MIN_WINDOW_HEIGTH,
    MIN_WINDOW_WIDTH,
    TICK_DURATION,
    GAME_SPEED
)


class Tetris():

    def __init__(self):
        self.state = dict()
        self.matrix = [[' ' for x in range(MATRIX_WIDTH)] for y in range(MATRIX_HEIGHT)]
        self.prev_time = None
        self.prev_activation_time = None
        self.curr_tetrimino = None
        self.input = None

    def main(self, stdscr):
        self._print_screen(stdscr)

        while True:
            tick_start_time = Tetris._get_curr_time()

            self.input = stdscr.getch()
            if self.input == ord('q'):
                break

            self._update(tick_start_time)
            self._sleep_if_possible(tick_start_time)

            self._print_matrix(stdscr)

    def _print_screen(self, stdscr):
        self._assert_window_size(stdscr)
        stdscr.clear()
        curses.curs_set(False)
        stdscr.nodelay(True)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        stdscr.addstr(0, 0, '          TETRIS          ', curses.color_pair(1))

        for y in range(MATRIX_HEIGHT):
            stdscr.addstr(y + 1, 0, ' ', curses.color_pair(1))
            stdscr.addstr(y + 1, MATRIX_WIDTH + 1, ' ', curses.color_pair(1))

        for x in range(MATRIX_WIDTH+2):
            stdscr.addstr(MATRIX_HEIGHT + 1, x, ' ', curses.color_pair(1))

        self._print_matrix(stdscr)

    def _update(self, tick_start_time):
        down = self._is_time_to_go_down(tick_start_time)

        if self.curr_tetrimino is None:
            self.curr_tetrimino = Tetrimino()
            self.curr_tetrimino.position = (0, MATRIX_WIDTH//2 - self.curr_tetrimino.get_width()//2)
            self._put_curr_tetrimino_in_matrix()
        elif down and self.curr_tetrimino.get_higher_y_coord() < MATRIX_HEIGHT:
            self._del_curr_tetrimino_from_matrix()
            y, x = self.curr_tetrimino.position
            self.curr_tetrimino.position = (y+1, x)
            self._put_curr_tetrimino_in_matrix()
        elif down and self.curr_tetrimino.get_higher_y_coord() == MATRIX_HEIGHT:
            self.curr_tetrimino = None

    def _put_curr_tetrimino_in_matrix(self):
        y_offset, x_offset = self.curr_tetrimino.position
        for y in range(self.curr_tetrimino.get_height()):
            for x in range(self.curr_tetrimino.get_width()):
                self.matrix[y_offset + y][x_offset + x] = self.curr_tetrimino.get_shape_matrix()[y][x]

    def _del_curr_tetrimino_from_matrix(self):
        y_offset, x_offset = self.curr_tetrimino.position
        for y in range(self.curr_tetrimino.get_height()):
            for x in range(self.curr_tetrimino.get_width()):
                self.matrix[y_offset + y][x_offset + x] = ' '

    def _is_time_to_go_down(self, tick_start_time):
        down = (self.prev_activation_time is None  # is the beginning of the game
                or tick_start_time - self.prev_activation_time > GAME_SPEED  # time on the current row is up
                or self.curr_tetrimino is None)  # the previous tetrimino reach the floor

        if down:
            self.prev_activation_time = tick_start_time

        return down

    def _sleep_if_possible(self, tick_start_time):
        if self.prev_time is not None:
            elapsed_time = tick_start_time - self.prev_time
            if elapsed_time < TICK_DURATION:
                time.sleep((TICK_DURATION-elapsed_time) / 1000)

        self.prev_time = tick_start_time

    def _assert_window_size(self, stdscr):
        heigth, width = stdscr.getmaxyx()
        if heigth < MIN_WINDOW_HEIGTH or width < MIN_WINDOW_WIDTH:
            raise Exception('The window is too small')

    def _print_matrix(self, stdscr):
        y_start, x_start = MATRIX_POS

        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                stdscr.addstr(y_start + y, x_start + x, cell, curses.color_pair(2))

        stdscr.refresh()

    @staticmethod
    def _get_curr_time():
        return time.time() * 1000


if __name__ == "__main__":
    curses.wrapper(Tetris().main)
