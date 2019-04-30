#!/usr/bin/env python3

import curses
import time

from screen import Screen
from inputaction import InputAction
from matrix import Matrix
from tetrimino import Tetrimino
from config import (
    TICK_DURATION,
    GAME_SPEED
)


class Tetris():

    def __init__(self):
        self._screen = Screen()
        self._matrix = Matrix()
        self._prev_activation_time = None
        self._curr_tetrimino = None
        self._exit = False

    def main(self, stdscr):
        self._screen.print_tetris(stdscr)

        while not self._exit:
            tick_start_time = Tetris._get_curr_time()
            actions = self.get_input_actions(stdscr.getch(), tick_start_time)

            self._update(actions)
            self._sleep_until_end_of_tick(tick_start_time)

            self._screen.print_tetris_matrix(self._matrix.get_matrix(), stdscr)

    def get_input_actions(self, input_char, tick_start_time):
        actions = []

        user_action = InputAction.get_action(input_char)
        if user_action is not None:
            actions.append(user_action)

        if self._tetrimino_should_go_down(tick_start_time):
            actions.append(InputAction.DOWN)

        return actions

    def _update(self, actions):
        for action in actions:
            if self._curr_tetrimino is None:
                self._curr_tetrimino, game_over = self._matrix.insert_new_tetrimino()
                if game_over:
                    # TODO implement a more friendly game over
                    self._exit = True
                    break

            if action in [InputAction.DOWN, InputAction.LEFT, InputAction.RIGHT]:
                success = self._matrix.move_tetrimino(self._curr_tetrimino, action)

                if not success and action == InputAction.DOWN:
                    # The tetrimino could not be moved down, which means it reached the bottom
                    self._matrix.remove_completed_rows(self._curr_tetrimino)
                    self._curr_tetrimino = None

            elif action == InputAction.ROTATE:
                self._matrix.rotate_tetrimino(self._curr_tetrimino)

            elif action == InputAction.QUIT:
                self._exit = True
                break

    def _tetrimino_should_go_down(self, tick_start_time):
        down = (self._prev_activation_time is None  # is the beginning of the game
                or tick_start_time - self._prev_activation_time > GAME_SPEED  # time on the current row is up
                or self._curr_tetrimino is None)  # the previous tetrimino reach the floor

        if down:
            self._prev_activation_time = tick_start_time

        return down

    def _sleep_until_end_of_tick(self, tick_start_time):
        elapsed_time = self._get_curr_time() - tick_start_time
        if elapsed_time < TICK_DURATION:
            time.sleep((TICK_DURATION - elapsed_time) / 1000)

    @staticmethod
    def _get_curr_time():
        return time.time() * 1000


if __name__ == "__main__":
    curses.wrapper(Tetris().main)
