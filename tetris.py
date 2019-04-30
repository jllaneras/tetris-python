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
        self.prev_activation_time = None
        self.curr_tetrimino = None
        self.exit = False

    def main(self, stdscr):
        self._screen.print_tetris(stdscr)

        while not self.exit:
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

        if self._is_time_to_go_down(tick_start_time):
            actions.append(InputAction.DOWN)

        return actions

    def _update(self, actions):
        for action in actions:
            if self.curr_tetrimino is None:
                self.curr_tetrimino = Tetrimino()
                start_position = self._matrix.get_start_position(self.curr_tetrimino)

                if self._matrix.collisions_found(self.curr_tetrimino, start_position):
                    # If there is a collision just after putting a new tetrimino in the screen then it's game over
                    # TODO implement a more friendly game over
                    self.exit = True
                    return
                else:
                    self.curr_tetrimino.position = start_position
                    self._matrix.insert_tetrimino(self.curr_tetrimino)

            if action in [InputAction.DOWN, InputAction.LEFT, InputAction.RIGHT]:
                new_position = self._calculate_new_tetrimino_position(action)

                if self._matrix.collisions_found(self.curr_tetrimino, new_position):
                    if action == InputAction.DOWN:
                        # The current tetrimino reached the bottom
                        self._matrix.remove_completed_rows(self.curr_tetrimino)
                        self.curr_tetrimino = None
                else:
                    self._matrix.remove_tetrimino(self.curr_tetrimino)
                    self.curr_tetrimino.position = new_position
                    self._matrix.insert_tetrimino(self.curr_tetrimino)

            elif action == InputAction.ROTATE:
                if not self._matrix.collisions_found(self.curr_tetrimino, self.curr_tetrimino.position, rotated=True):
                    self._matrix.remove_tetrimino(self.curr_tetrimino)
                    self.curr_tetrimino.rotate()
                    self._matrix.insert_tetrimino(self.curr_tetrimino)

            elif action == InputAction.QUIT:
                self.exit = True

    def _calculate_new_tetrimino_position(self, action):
        if action == InputAction.LEFT:
            return self.curr_tetrimino.get_pos_left()
        elif action == InputAction.DOWN:
            return self.curr_tetrimino.get_pos_down()
        elif action == InputAction.RIGHT:
            return self.curr_tetrimino.get_pos_right()
        else:
            return self.curr_tetrimino.position

    def _is_time_to_go_down(self, tick_start_time):
        down = (self.prev_activation_time is None  # is the beginning of the game
                or tick_start_time - self.prev_activation_time > GAME_SPEED  # time on the current row is up
                or self.curr_tetrimino is None)  # the previous tetrimino reach the floor

        if down:
            self.prev_activation_time = tick_start_time

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
