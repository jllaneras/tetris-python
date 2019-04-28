import curses
import time

from tetrimino import Tetrimino
from constants import (
        MIN_WINDOW_HEIGTH,
        MIN_WINDOW_WIDTH,
        MATRIX_WIDTH,
        MATRIX_HEIGTH,
        TICK_DURATION,
        GAME_SPEED
)

state = dict()


def main(stdscr):
    state['matrix'] = [[' ' for x in range(MATRIX_WIDTH)] for y in range(MATRIX_HEIGTH)]
    state['exit'] = False
    state['prev_time'] = None
    state['prev_activation_time'] = None
    state['curr_tetrimino'] = None

    init(stdscr)

    while not state['exit']:
        ch = stdscr.getch()
        if ch == ord('q'):
            state['exit'] = True

        curr_time = get_curr_time()
        down = is_time_to_go_down(curr_time)
        if down:
            state['prev_activation_time'] = curr_time

        update(down, ch)
        sleep_if_possible(state['prev_time'], curr_time)
        state['prev_time'] = curr_time

        print_matrix(state['matrix'], stdscr, 1, 0)
        stdscr.refresh()


def init(stdscr):
    assert_window_size(stdscr)
    stdscr.clear()
    curses.curs_set(False)    
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
    
    stdscr.addstr(0, 0, '         TETRIS         ', curses.color_pair(1))
    
    print_matrix(state['matrix'], stdscr, 1, 0)


def update(down, ch):
    if state['curr_tetrimino'] is None:
        #curr_tetrimino = Tetrimino.get_random_shape()
        curr_tetrimino = Tetrimino()
        curr_tetrimino.position = (0, MATRIX_WIDTH//2 - curr_tetrimino.get_width()//2)
        put_tetrominoe(curr_tetrimino, state['matrix'])
        state['curr_tetrimino'] = curr_tetrimino
    elif down and state['curr_tetrimino'].get_higher_y_coord() < MATRIX_HEIGTH:
        curr_tetrimino = state['curr_tetrimino']
        remove_tetrominoe(curr_tetrimino, state['matrix'])
        y, x = curr_tetrimino.position;
        curr_tetrimino.position = (y+1, x)
        put_tetrominoe(state['curr_tetrimino'], state['matrix'])
    elif down and state['curr_tetrimino'].get_higher_y_coord() == MATRIX_HEIGTH:
        state['curr_tetrimino'] = None


def put_tetrominoe(tetrominoe, matrix):
    y_offset, x_offset = tetrominoe.position
    for y in range(tetrominoe.get_height()):
        for x in range(tetrominoe.get_width()):
            matrix[y_offset + y][x_offset + x] = tetrominoe.get_shape_matrix()[y][x]


def remove_tetrominoe(tetrominoe, matrix):
    y_offset, x_offset = tetrominoe.position
    for y in range(tetrominoe.get_height()):
        for x in range(tetrominoe.get_width()):
            matrix[y_offset + y][x_offset + x] = ' '


def is_time_to_go_down(curr_time):
    return (state['prev_activation_time'] is None
            or curr_time - state['prev_activation_time'] > GAME_SPEED
            or state['curr_tetrimino'] is None)


def get_curr_time():
    return time.time() * 1000


def sleep_if_possible(prev_time, curr_time):
    if prev_time == None:
        return

    elapsed_time = curr_time - prev_time
    if elapsed_time < TICK_DURATION:
        time.sleep((TICK_DURATION-elapsed_time) / 1000)


def assert_window_size(stdscr):
    heigth, width = stdscr.getmaxyx()
    if heigth < MIN_WINDOW_HEIGTH or width < MIN_WINDOW_WIDTH:
        raise Exception('The window is too small')


def print_matrix(matrix, stdscr, y_start, x_start):
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            stdscr.addstr(y_start + y, x_start + x, cell, curses.color_pair(2))


if __name__ == "__main__": 
    curses.wrapper(main)
