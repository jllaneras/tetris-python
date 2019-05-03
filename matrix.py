from config import TETRIS_MATRIX_HEIGHT, TETRIS_MATRIX_WIDTH
from inputaction import InputAction


class Matrix():

    def __init__(self):
        self._matrix = [[None for x in range(TETRIS_MATRIX_WIDTH)] for y in range(TETRIS_MATRIX_HEIGHT)]

    def get_matrix(self):
        return self._matrix

    def get_start_position(self, tetrimino):
        return 0, TETRIS_MATRIX_WIDTH // 2 - tetrimino.get_width() // 2

    def insert_new_tetrimino(self, new_tetrimino):
        start_position = self.get_start_position(new_tetrimino)
        game_over = False

        if self._collisions_found(new_tetrimino, start_position):
            game_over = True
        else:
            new_tetrimino.position = start_position
            self._insert_tetrimino(new_tetrimino)

        return game_over

    def move_tetrimino(self, tetrimino, action):
        success = False
        new_position = self._calculate_new_tetrimino_position(tetrimino, action)

        if not self._collisions_found(tetrimino, new_position):
            self._remove_tetrimino(tetrimino)
            tetrimino.position = new_position
            self._insert_tetrimino(tetrimino)
            success = True

        return success

    def rotate_tetrimino(self, tetrimino):
        success = False

        if not self._collisions_found(tetrimino, tetrimino.position, rotated=True):
            self._remove_tetrimino(tetrimino)
            tetrimino.rotate()
            self._insert_tetrimino(tetrimino)
            success = True

        return success

    def remove_completed_rows(self, tetrimino):
        y_start, _ = tetrimino.position
        y_end = y_start + tetrimino.get_height()
        removed_rows = 0

        for y in range(y_start, y_end):
            complete = True

            for x in range(TETRIS_MATRIX_WIDTH):
                # The call to _coord_out_of_bounds is needed because the matrix of the tetrimino may have empty rows
                # TODO find a more elegant way to do this
                if self._coord_out_of_bounds(y, x) or self._matrix[y][x] is None:
                    complete = False
                    break

            if complete:
                self._matrix.pop(y)
                self._matrix.insert(0, [None for x in range(TETRIS_MATRIX_WIDTH)])
                removed_rows += 1

        return removed_rows

    def _collisions_found(self, tetrimino, new_position, rotated=False):
        # TODO find a more elegant way to check for collisions
        if tetrimino.in_matrix():
            # Remove the tetrimino from the matrix to be able to calculate collisions for its new position/shape
            self._remove_tetrimino(tetrimino)

        collisions_found = self._collisions_found_with_other_tetriminos(tetrimino, new_position, rotated)

        if tetrimino.in_matrix():
            # Put back the tetrimino in the matrix after the collisions have been calculated for its new position/shape
            self._insert_tetrimino(tetrimino)

        return collisions_found

    def _collisions_found_with_other_tetriminos(self, tetrimino, new_position, rotated):
        if self._tetrimino_out_of_bounds(tetrimino, new_position, rotated):
            return True

        tetrimino_matrix = tetrimino.get_cell_matrix(rotated)
        y_offset, x_offset = new_position
        # Check if each cell in the tetrimino shape matrix doesn't clash with an existing tetrimino in the tetris matrix
        for y in range(tetrimino.get_height(rotated)):
            for x in range(tetrimino.get_width(rotated)):
                if tetrimino_matrix[y][x] is not None and self._matrix[y_offset + y][x_offset + x] is not None:
                    return True

        return False

    def _tetrimino_out_of_bounds(self, tetrimino, new_position, rotated):
        tetrimino_matrix = tetrimino.get_cell_matrix(rotated)
        y_offset, x_offset = new_position

        # TODO this loop keeps repeating
        for y in range(tetrimino.get_height(rotated)):
            for x in range(tetrimino.get_width(rotated)):
                if tetrimino_matrix[y][x] is not None and self._coord_out_of_bounds(y_offset + y, x_offset + x):
                    return True

        return False

    def _coord_out_of_bounds(self, y, x):
        return y >= TETRIS_MATRIX_HEIGHT or y < 0 or x >= TETRIS_MATRIX_WIDTH or x < 0

    def _insert_tetrimino(self, tetrimino):
        y_offset, x_offset = tetrimino.position

        for y in range(tetrimino.get_height()):
            for x in range(tetrimino.get_width()):
                tetrimino_cell = tetrimino.get_cell_matrix()[y][x]
                if tetrimino_cell is not None:
                    self._matrix[y_offset + y][x_offset + x] = tetrimino_cell

    def _remove_tetrimino(self, tetrimino):
        y_offset, x_offset = tetrimino.position

        for y in range(tetrimino.get_height()):
            for x in range(tetrimino.get_width()):
                tetrimino_cell = tetrimino.get_cell_matrix()[y][x]
                if tetrimino_cell is not None:
                    self._matrix[y_offset + y][x_offset + x] = None

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
