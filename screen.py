import curses

from config import (
    TETRIS_MATRIX_WIDTH,
    TETRIS_MATRIX_HEIGHT
)

MATRIX_POS = (1, 1)  # (y, x) position of the Tetrix matrix on the screen
TETRIS_WIDTH = TETRIS_MATRIX_WIDTH + 2  # takes the lateral borders into account
TETRIS_HEIGHT = TETRIS_MATRIX_HEIGHT + 2  # takes the top/bottom borders into account

class Screen():

    def init_tetris(self, stdscr):
        self._assert_window_size(stdscr)

        self._init_curses(stdscr)

        self._print_tetris_score(stdscr, 0)
        self._print_lateral_walls(stdscr)
        self._print_bottom_wall(stdscr)

        stdscr.refresh()

    def render_tetris(self, tetris_matrix, score, stdscr):
        y_offset, x_offset = MATRIX_POS

        for y, row in enumerate(tetris_matrix):
            for x, cell in enumerate(row):
                stdscr.addstr(y_offset + y, x_offset + x, cell, curses.color_pair(2))

        self._print_tetris_score(stdscr, score)

        stdscr.refresh()

    def _init_curses(self, stdscr):
        stdscr.clear()
        curses.curs_set(False)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def _assert_window_size(self, stdscr):
        heigth, width = stdscr.getmaxyx()
        if heigth < TETRIS_HEIGHT or width < TETRIS_WIDTH:
            raise Exception('The terminal window is too small')

    def _print_tetris_score(self, stdscr, score):
        header = ' Score: {}'.format(score)
        if len(header) < TETRIS_WIDTH:
            header = header + (TETRIS_WIDTH - len(header)) * ' '
        stdscr.addstr(0, 0, header, curses.color_pair(1))

    def _print_lateral_walls(self, stdscr):
        for y in range(TETRIS_MATRIX_HEIGHT):
            stdscr.addstr(y + 1, 0, ' ', curses.color_pair(1))
            stdscr.addstr(y + 1, TETRIS_MATRIX_WIDTH + 1, ' ', curses.color_pair(1))

    def _print_bottom_wall(self, stdscr):
        for x in range(TETRIS_WIDTH):
            stdscr.addstr(TETRIS_HEIGHT - 1, x, ' ', curses.color_pair(1))
