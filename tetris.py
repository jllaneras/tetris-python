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
        self._row_time = 0
        self._curr_tetrimino = Tetrimino()
        self._next_tetrimino = Tetrimino()
        self._last_score = 0
        self._total_score = 0
        self._exit = False
        self._game_paused = False

    def main(self, stdscr):
        self._screen.init_tetris(stdscr)

        while not self._exit:
            tick_start_time = Tetris._get_curr_time()
            actions = self._get_input(stdscr.getch())

            if not self._curr_tetrimino.in_matrix():
                game_over = self._matrix.insert_new_tetrimino(self._curr_tetrimino)
                if game_over:
                    self._exit = True
            else:
                self._process_input(actions)
                self._sleep_until_end_of_tick(tick_start_time)

            self._screen.render_tetris(
                self._matrix.get_matrix(),
                self._total_score,
                self._last_score,
                self._next_tetrimino, 
                self._game_paused,
                stdscr)

    def get_score(self):
        return self._total_score

    def _get_input(self, input_char):
        actions = []

        user_action = InputAction.get_action(input_char)
        if user_action is not None:
            actions.append(user_action)

        if self._tetrimino_should_go_down():
            actions.append(InputAction.DOWN)

        return actions

    def _process_input(self, actions):
        for action in actions:
            if not self._game_paused and action in [InputAction.DOWN, InputAction.LEFT, InputAction.RIGHT]:
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

            elif not self._game_paused and action == InputAction.ROTATE:
                self._matrix.rotate_tetrimino(self._curr_tetrimino)

            elif action == InputAction.QUIT:
                self._exit = True
                break
            
            elif action == InputAction.PAUSE:
                self._game_paused = True

            elif action == InputAction.CONTINUE:
                self._game_paused = False

    def _tetrimino_should_go_down(self):
        if self._game_paused:
            return False

        if self._row_time >= GAME_SPEED:
            self._row_time = 0  # reset row time counter
            return True
        else:
            self._row_time += TICK_DURATION
            return False

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
