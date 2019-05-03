import curses

from tetrimino import TetriminoCell
from config import (
    TETRIS_MATRIX_WIDTH,
    TETRIS_MATRIX_HEIGHT
)

# (y, x) position of the Tetrix matrix on the screen
TETRIS_MATRIX_POS = (1, 1)

WALL_CHAR = '\u2588'
WALL_COLOR_PAIR = curses.COLOR_GREEN

# takes the lateral walls into account
TETRIS_BOX_WIDTH = TETRIS_MATRIX_WIDTH * TetriminoCell.width + 2 * len(WALL_CHAR)

# takes the top/bottom borders into account
TETRIS_BOX_HEIGHT = TETRIS_MATRIX_HEIGHT * TetriminoCell.height + 2 * len(WALL_CHAR)

HELP_AREA_WIDTH = 25

GAME_HEIGHT = TETRIS_BOX_HEIGHT
GAME_WIDTH = TETRIS_BOX_WIDTH + HELP_AREA_WIDTH

SCORE_COLOR_PAIR = 8

class Screen():

    def init_tetris(self, stdscr):
        self._assert_window_size(stdscr)

        self._init_curses(stdscr)

        self._render_tetris_score(stdscr, 0)
        self._render_lateral_walls(stdscr)
        self._render_bottom_wall(stdscr)
        self._render_help(stdscr)

        stdscr.refresh()

    def render_tetris(self, tetris_matrix, score, stdscr):
        y_offset, x_offset = TETRIS_MATRIX_POS

        for y, row in enumerate(tetris_matrix):
            for x, cell in enumerate(row):
                if cell is not None:
                    stdscr.addstr(y_offset + y*TetriminoCell.height, x_offset + x*TetriminoCell.width, cell.str, curses.color_pair(cell.color))
                else:
                    stdscr.addstr(y_offset + y*TetriminoCell.height, x_offset + x*TetriminoCell.width, ' ' * TetriminoCell.width, curses.color_pair(1))

        self._render_tetris_score(stdscr, score)

        stdscr.refresh()

    def _assert_window_size(self, stdscr):
        heigth, width = stdscr.getmaxyx()
        if heigth < GAME_HEIGHT or width < GAME_WIDTH:
            raise Exception('The terminal window is too small')

    def _init_curses(self, stdscr):
        stdscr.clear()
        curses.curs_set(False)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        # Color range from 1 to 7
        curses.init_pair(curses.COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_pair(SCORE_COLOR_PAIR, curses.COLOR_BLACK, curses.COLOR_GREEN)

    def _render_tetris_score(self, stdscr, score):
        header = ' Score: {}'.format(score)
        if len(header) < TETRIS_BOX_WIDTH:
            header = header + (TETRIS_BOX_WIDTH - len(header)) * ' '
        stdscr.addstr(0, 0, header, curses.color_pair(SCORE_COLOR_PAIR))

    def _render_lateral_walls(self, stdscr):
        for y in range(1, GAME_HEIGHT):
            stdscr.addstr(y, 0, WALL_CHAR, curses.color_pair(WALL_COLOR_PAIR))
            stdscr.addstr(y, TETRIS_BOX_WIDTH - 1, WALL_CHAR, curses.color_pair(WALL_COLOR_PAIR))

    def _render_bottom_wall(self, stdscr):
        for x in range(TETRIS_BOX_WIDTH):
            stdscr.addstr(GAME_HEIGHT - 1, x, WALL_CHAR, curses.color_pair(curses.COLOR_GREEN))

    def _render_help(self, stdscr):
        y = GAME_HEIGHT - 10
        x = TETRIS_BOX_WIDTH + 2
        help_lines = [
            '\u2190 = move left',
            '\u2192 = move right',
            '\u2193 = move down',
            '\u2191 = rotate',
            '',
            'Ctrl+S = pause',
            'Ctrl+Q = continue',
            '',
            'Q = exit'
        ]

        for i, line in enumerate(help_lines):
            stdscr.addstr(y + i, x, line, curses.color_pair(curses.COLOR_GREEN))
