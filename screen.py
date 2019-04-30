import curses
from constants import (
    TETRIS_MATRIX_WIDTH,
    TETRIS_MATRIX_HEIGHT,
    MATRIX_POS,
    MIN_WINDOW_HEIGTH,
    MIN_WINDOW_WIDTH
)

class Screen():

    def print_tetris(self, stdscr):
        self._assert_window_size(stdscr)
        stdscr.clear()
        curses.curs_set(False)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        header = 'TETRIS'
        header = (TETRIS_MATRIX_WIDTH + 2 - len(header)) // 2 * ' ' + header
        header = header + (TETRIS_MATRIX_WIDTH + 2 - len(header)) * ' '

        stdscr.addstr(0, 0, header, curses.color_pair(1))

        for y in range(TETRIS_MATRIX_HEIGHT):
            stdscr.addstr(y + 1, 0, ' ', curses.color_pair(1))
            stdscr.addstr(y + 1, TETRIS_MATRIX_WIDTH + 1, ' ', curses.color_pair(1))

        for x in range(TETRIS_MATRIX_WIDTH + 2):
            stdscr.addstr(TETRIS_MATRIX_HEIGHT + 1, x, ' ', curses.color_pair(1))

    def print_tetris_matrix(self, tetris_matrix, stdscr):
        y_start, x_start = MATRIX_POS

        for y, row in enumerate(tetris_matrix):
            for x, cell in enumerate(row):
                stdscr.addstr(y_start + y, x_start + x, cell, curses.color_pair(2))

        stdscr.refresh()

    def _assert_window_size(self, stdscr):
        heigth, width = stdscr.getmaxyx()
        if heigth < MIN_WINDOW_HEIGTH or width < MIN_WINDOW_WIDTH:
            raise Exception('The terminal window is too small')
