from tetriminoshape import TetriminoShape
from config import TETRIS_MATRIX_WIDTH


class Tetrimino():

    def __init__(self):
        self._shape = TetriminoShape.get_random()
        self._shape_matrix = self._shape.get_matrix()
        # The tetrimino is placed in the middle of the top row
        self._position = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def in_matrix(self):
        return self._position is not None

    def get_shape_matrix(self, rotated=False):
        if rotated:
            return self._calculate_rotated_matrix()
        else:
            return self._shape_matrix

    def get_width(self, rotated=False):
        if rotated:
            return self.get_height()
        else:
            return len(self.get_shape_matrix()[0])

    def get_height(self, rotated=False):
        if rotated:
            return self.get_width()
        else:
            return len(self.get_shape_matrix())

    def get_higher_y_coord(self):
        y, _ = self.position
        return y + self.get_height()

    def get_higher_x_coord(self):
        _, x = self.position
        return x + self.get_width()

    def rotate(self):
        self._shape_matrix = self._calculate_rotated_matrix()

    def _calculate_rotated_matrix(self):
        rotated_matrix = []

        for i in range(self.get_width()):
            row = []
            for j in range(self.get_height()):
                row.append(self._shape_matrix[self.get_height() - 1 - j][i])
            rotated_matrix.append(row)

        return rotated_matrix
