from tetriminoshape import TetriminoShape

_TETRIMINO_CELL_CHAR = '\u2593'


class TetriminoCell():
    def __init__(self, color):
        self.char = _TETRIMINO_CELL_CHAR
        self.color = color

    def __repr__(self):
        return 'char=%s, color=%s' % (self.char, self.color)

class Tetrimino():

    def __init__(self):
        self._shape = TetriminoShape.get_random()
        self._cell_matrix = self._build_cell_matrix(self._shape.get_matrix(), self._shape.get_color())
        self._position = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def in_matrix(self):
        return self._position is not None

    def get_cell_matrix(self, rotated=False):
        if rotated:
            return self._calculate_rotated_matrix()
        else:
            return self._cell_matrix

    def get_width(self, rotated=False):
        if rotated:
            return self.get_height()
        else:
            return len(self.get_cell_matrix()[0])

    def get_height(self, rotated=False):
        if rotated:
            return self.get_width()
        else:
            return len(self.get_cell_matrix())

    def rotate(self):
        self._cell_matrix = self._calculate_rotated_matrix()

    def _calculate_rotated_matrix(self):
        rotated_matrix = []

        for i in range(self.get_width()):
            row = []
            for j in range(self.get_height()):
                row.append(self._cell_matrix[self.get_height() - 1 - j][i])
            rotated_matrix.append(row)

        return rotated_matrix

    def _build_cell_matrix(self, shape_matrix, color):
        return [[TetriminoCell(color) if cell == 'X' else None for cell in row] for row in shape_matrix]
