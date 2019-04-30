from config import TETRIS_MATRIX_HEIGHT, TETRIS_MATRIX_WIDTH


class Matrix():

    def __init__(self):
        self._matrix = [[' ' for x in range(TETRIS_MATRIX_WIDTH)] for y in range(TETRIS_MATRIX_HEIGHT)]

    def get_matrix(self):
        return self._matrix;

    def get_start_position(self, tetrimino):
        return 0, TETRIS_MATRIX_WIDTH // 2 - tetrimino.get_width() // 2

    def collisions_found(self, tetrimino, new_position, rotated=False):
        if tetrimino.is_visible():
            # Remove tetrimino from matrix to check for collisions if it's moved to new position and/or its shape is
            # changed (when rotated is True)
            self.remove_tetrimino(tetrimino)

        collisions_found = self._collisions_found(tetrimino, new_position, rotated)

        if tetrimino.is_visible():
            # Put back tetrimino in matrix after collisions have been calculated for its new position or shape
            self.insert_tetrimino(tetrimino)

        return collisions_found

    def _collisions_found(self,  tetrimino, new_position, rotated):
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
