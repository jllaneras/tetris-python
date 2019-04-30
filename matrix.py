from config import TETRIS_MATRIX_HEIGHT, TETRIS_MATRIX_WIDTH
from tetrimino import Tetrimino
from inputaction import InputAction


class Matrix():

    def __init__(self):
        self._matrix = [[' ' for x in range(TETRIS_MATRIX_WIDTH)] for y in range(TETRIS_MATRIX_HEIGHT)]

    def get_matrix(self):
        return self._matrix

    def get_start_position(self, tetrimino):
        return 0, TETRIS_MATRIX_WIDTH // 2 - tetrimino.get_width() // 2

    def collisions_found(self, tetrimino, new_position, rotated=False):
        if tetrimino.in_matrix():
            # Remove the tetrimino from the matrix to be able to calculate collisions for its new position/shape
            self.remove_tetrimino(tetrimino)

        collisions_found = self._collisions_found(tetrimino, new_position, rotated)

        if tetrimino.in_matrix():
            # Put back the tetrimino in the matrix after the collisions have been calculated for its new position/shape
            self.insert_tetrimino(tetrimino)

        return collisions_found

    def _collisions_found(self, tetrimino, new_position, rotated):
        tetrimino_matrix = tetrimino.get_shape_matrix(rotated)

        if self.tetrimino_out_of_bounds(tetrimino_matrix, new_position):
            return True

        y_offset, x_offset = new_position
        # Check if each cell in the tetrimino shape matrix doesn't clash with an existing tetrimino in the tetris matrix
        for y in range(len(tetrimino_matrix)):
            for x in range(len(tetrimino_matrix[0])):
                if tetrimino_matrix[y][x] != ' ' and self._matrix[y_offset + y][x_offset + x] != ' ':
                    return True

        return False

    def tetrimino_out_of_bounds(self, tetrimino_matrix, new_position):
        y, x = new_position
        tetrimino_height = len(tetrimino_matrix)
        tetrimino_width = len(tetrimino_matrix[0])

        return (y + tetrimino_height - 1) >= TETRIS_MATRIX_HEIGHT \
               or x < 0 \
               or (x + tetrimino_width - 1) >= TETRIS_MATRIX_WIDTH

    def insert_new_tetrimino(self):
        new_tetrimino = Tetrimino()
        start_position = self.get_start_position(new_tetrimino)
        game_over = False

        if self.collisions_found(new_tetrimino, start_position):
            game_over = True
        else:
            new_tetrimino.position = start_position
            self.insert_tetrimino(new_tetrimino)

        return new_tetrimino, game_over

    def insert_tetrimino(self, tetrimino):
        y_offset, x_offset = tetrimino.position

        for y in range(tetrimino.get_height()):
            for x in range(tetrimino.get_width()):
                tetrimino_cell = tetrimino.get_shape_matrix()[y][x]
                if tetrimino_cell != ' ':
                    self._matrix[y_offset + y][x_offset + x] = tetrimino_cell

    def remove_tetrimino(self, tetrimino):
        y_offset, x_offset = tetrimino.position

        for y in range(tetrimino.get_height()):
            for x in range(tetrimino.get_width()):
                tetrimino_cell = tetrimino.get_shape_matrix()[y][x]
                if tetrimino_cell != ' ':
                    self._matrix[y_offset + y][x_offset + x] = ' '

    def move_tetrimino(self, tetrimino, action):
        success = False
        new_position = self._calculate_new_tetrimino_position(tetrimino, action)

        if not self.collisions_found(tetrimino, new_position):
            self.remove_tetrimino(tetrimino)
            tetrimino.position = new_position
            self.insert_tetrimino(tetrimino)
            success = True

        return success

    def _calculate_new_tetrimino_position(self, tetrimino, action):
        y, x = tetrimino.position

        if action == InputAction.LEFT:
            return y, x - 1
        elif action == InputAction.DOWN:
            return y + 1, x
        elif action == InputAction.RIGHT:
            return y, x + 1
        else:
            return tetrimino.position

    def rotate_tetrimino(self, tetrimino):
        success = False

        if not self.collisions_found(tetrimino, tetrimino.position, rotated=True):
            self.remove_tetrimino(tetrimino)
            tetrimino.rotate()
            self.insert_tetrimino(tetrimino)
            success = True

        return success

    def remove_completed_rows(self, tetrimino):
        y_start, _ = tetrimino.position
        y_end = y_start + tetrimino.get_height()

        for y in range(y_start, y_end):
            complete = True

            for x in range(TETRIS_MATRIX_WIDTH):
                if self._matrix[y][x] == ' ':
                    complete = False
                    break

            if complete:
                self._matrix.pop(y)
                self._matrix.insert(0, [' ' for x in range(TETRIS_MATRIX_WIDTH)])
