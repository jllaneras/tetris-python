from tetriminoshape import TetriminoShape
from config import TETRIS_MATRIX_WIDTH


class Tetrimino():

    def __init__(self):
        self.__shape = TetriminoShape.get_random()
        self.__shape_matrix = self.__shape.get_matrix()
        # The tetrimino is placed in the middle of the top row
        self.__position = None

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

    def is_visible(self):
        return self.__position is not None

    def get_shape_matrix(self, rotated=False):
        if rotated:
            return self._calculate_rotated_matrix()
        else:
            return self.__shape_matrix

    def get_width(self):
        return len(self.get_shape_matrix()[0])

    def get_height(self):
        return len(self.get_shape_matrix())

    def get_higher_y_coord(self):
        y, _ = self.position
        return y + self.get_height()

    def get_higher_x_coord(self):
        _, x = self.position
        return x + self.get_width()

    def get_pos_left(self):
        y, x = self.__position
        return y, x - 1

    def get_pos_right(self):
        y, x = self.__position
        return y, x + 1

    def get_pos_down(self):
        y, x = self.__position
        return y + 1, x

    def rotate(self):
        self.__shape_matrix = self._calculate_rotated_matrix()

    def _calculate_rotated_matrix(self):
        rotated_matrix = []

        for i in range(len(self.__shape_matrix[0])):
            row = []
            for j in range(len(self.__shape_matrix)):
                row.append(self.__shape_matrix[len(self.__shape_matrix) - 1 - j][i])
            rotated_matrix.append(row)

        return rotated_matrix