#!/usr/bin/env python3

import curses
import time

from tetrimino import Tetrimino
from screen import Screen
from inputaction import InputAction
from matrix import Matrix
from config import (
    TICK_DURATION,
    GAME_SPEED
)

_SCORES = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}


class Tetris():

    def __init__(self):
        self._screen = Screen()
        self._matrix = Matrix()
        self._prev_activation_time = None
        self._curr_tetrimino = Tetrimino()
        self._next_tetrimino = Tetrimino()
        self._last_score = 0
        self._total_score = 0
        self._exit = False

    def main(self, stdscr):
        self._screen.init_tetris(stdscr)

        while not self._exit:
            tick_start_time = Tetris._get_curr_time()
            actions = self._get_input_actions(stdscr.getch(), tick_start_time)

            self._update(actions)
            self._sleep_until_end_of_tick(tick_start_time)

            self._screen.render_tetris(
                self._matrix.get_matrix(),
                self._total_score,
                self._last_score,
                self._next_tetrimino, stdscr)

    def get_score(self):
        return self._total_score

    def _get_input_actions(self, input_char, tick_start_time):
        actions = []

        user_action = InputAction.get_action(input_char)
        if user_action is not None:
            actions.append(user_action)

        if self._tetrimino_should_go_down(tick_start_time):
            actions.append(InputAction.DOWN)

        return actions

    def _update(self, actions):
        for action in actions:
            if not self._curr_tetrimino.in_matrix():
                game_over = self._matrix.insert_new_tetrimino(self._curr_tetrimino)
                if game_over:
                    self._exit = True
                    break

            if action in [InputAction.DOWN, InputAction.LEFT, InputAction.RIGHT]:
                success = self._matrix.move_tetrimino(self._curr_tetrimino, action)

                if not success and action == InputAction.DOWN:
                    # The tetrimino could not be moved down, which means it reached the bottom
                    num_removed_rows = self._matrix.remove_completed_rows(self._curr_tetrimino)

                    curr_score = _SCORES[num_removed_rows]
                    if curr_score > 0:
                        self._last_score = curr_score
                        self._total_score += curr_score

                    self._curr_tetrimino = self._next_tetrimino
                    self._next_tetrimino = Tetrimino()

            elif action == InputAction.ROTATE:
                self._matrix.rotate_tetrimino(self._curr_tetrimino)

            elif action == InputAction.QUIT:
                self._exit = True
                break

    def _tetrimino_should_go_down(self, tick_start_time):
        go_down = (not self._curr_tetrimino.in_matrix()  # there is not a tetrimino in the screen
                or tick_start_time - self._prev_activation_time > GAME_SPEED)  # time on the current row is up

        if go_down:
            self._prev_activation_time = tick_start_time

        return go_down

    def _sleep_until_end_of_tick(self, tick_start_time):
        elapsed_time = self._get_curr_time() - tick_start_time
        if elapsed_time < TICK_DURATION:
            time.sleep((TICK_DURATION - elapsed_time) / 1000)

    @staticmethod
    def _get_curr_time():
        return time.time() * 1000


if __name__ == '__main__':
    tetris = Tetris()
    curses.wrapper(tetris.main)
    print('===========')
    print('GAME OVER')
    print('Your final score is: {}'.format(tetris.get_score()))
    print('===========')
