from tetriminoshape import TetriminoShape


class Tetrimino():

    def __init__(self, shape=None, position=None):
        if shape is None:
            self.__shape = TetriminoShape.get_random()
        else:
            self.__shape = shape

        self.__shape_matrix = self.__shape.get_matrix()
        self.__position = position

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position

    def get_shape_matrix(self, rotated=False):
        # TODO take rotated parameter into account
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
        # TODO
        pass