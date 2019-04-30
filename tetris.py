import curses
import time

from screen import Screen
from inputaction import InputAction

from tetrimino import Tetrimino
from config import (
    TETRIS_MATRIX_WIDTH,
    TETRIS_MATRIX_HEIGHT,
    TICK_DURATION,
    GAME_SPEED
)


class Tetris():

    def __init__(self):
        self.__screen = Screen()
        self.matrix = [[' ' for x in range(TETRIS_MATRIX_WIDTH)] for y in range(TETRIS_MATRIX_HEIGHT)]
        self.prev_activation_time = None
        self.curr_tetrimino = None
        self.exit = False

    def main(self, stdscr):
        self.__screen.print_tetris(stdscr)

        while not self.exit:
            tick_start_time = Tetris._get_curr_time()
            actions = self.get_input_actions(stdscr.getch(), tick_start_time)

            self._update(actions)
            self._sleep_until_end_of_tick(tick_start_time)

            self.__screen.print_tetris_matrix(self.matrix, stdscr)

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

                if self._collisions(self.curr_tetrimino.get_shape_matrix(), self.curr_tetrimino.position):
                    # If there is a collision just after putting a new tetrimino in the screen then it's game over
                    # TODO implement a more friendly game over
                    self.exit = True
                    return
                else:
                    self._put_curr_tetrimino_in_matrix()

            if action == InputAction.DOWN or action == InputAction.LEFT or action == InputAction.RIGHT:
                new_position = self._calculate_new_tetrimino_position(action)
                tetrimino_matrix = self.curr_tetrimino.get_shape_matrix()

                # Remove curr tetrimino from matrix to calculate colisions of new position
                self._del_curr_tetrimino_from_matrix()

                if self._collisions(tetrimino_matrix, new_position):
                    self._put_curr_tetrimino_in_matrix()

                    if action == InputAction.DOWN:
                        # The current tetrimino reached the bottom
                        self._remove_completed_rows()
                        self.curr_tetrimino = None
                else:
                    self.curr_tetrimino.position = new_position
                    self._put_curr_tetrimino_in_matrix()

            elif action == InputAction.ROTATE:
                # Remove curr tetrimino from matrix to calculate colisions of new position
                self._del_curr_tetrimino_from_matrix()

                rotated_tetrimino_matrix = self.curr_tetrimino.get_rotated_shape_matrix()
                if not self._collisions(rotated_tetrimino_matrix, self.curr_tetrimino.position):
                    self.curr_tetrimino.rotate()
                    self._put_curr_tetrimino_in_matrix()

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

    def _collisions(self, tetrimino_matrix, new_position):
        if self._tetrimino_out_of_bounds(tetrimino_matrix, new_position):
            return True

        y_offset, x_offset = new_position

        # Check if each cell in the tetrimino shape matrix doesn't clash with an existing tetrimino in the tetris matrix
        for y in range(len(tetrimino_matrix)):
            for x in range(len(tetrimino_matrix[0])):
                if tetrimino_matrix[y][x] != ' ' and self.matrix[y_offset+y][x_offset+x] != ' ':
                    return True

        return False

    def _tetrimino_out_of_bounds(self, tetrimino_matrix, new_position):
        y, x = new_position
        tetrimino_heigth = len(tetrimino_matrix)
        tetrimino_width = len(tetrimino_matrix[0])

        return (y + tetrimino_heigth - 1) >= TETRIS_MATRIX_HEIGHT \
               or x < 0 \
               or (x + tetrimino_width - 1) >= TETRIS_MATRIX_WIDTH

    def _put_curr_tetrimino_in_matrix(self):
        y_offset, x_offset = self.curr_tetrimino.position
        for y in range(self.curr_tetrimino.get_height()):
            for x in range(self.curr_tetrimino.get_width()):
                tetrimino_cell = self.curr_tetrimino.get_shape_matrix()[y][x]
                if tetrimino_cell != ' ':
                    self.matrix[y_offset + y][x_offset + x] = tetrimino_cell

    def _del_curr_tetrimino_from_matrix(self):
        y_offset, x_offset = self.curr_tetrimino.position
        for y in range(self.curr_tetrimino.get_height()):
            for x in range(self.curr_tetrimino.get_width()):
                tetrimino_cell = self.curr_tetrimino.get_shape_matrix()[y][x]
                if tetrimino_cell != ' ':
                    self.matrix[y_offset + y][x_offset + x] = ' '

    def _remove_completed_rows(self):
        y_offset, _ = self.curr_tetrimino.position

        for y in range(y_offset, y_offset + self.curr_tetrimino.get_height()):
            complete = True

            for x in range(TETRIS_MATRIX_WIDTH):
                if self.matrix[y][x] == ' ':
                    complete = False
                    break

            if complete:
                self.matrix.pop(y)
                self.matrix.insert(0, [' ' for x in range(TETRIS_MATRIX_WIDTH)])

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
