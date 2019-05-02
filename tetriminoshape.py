from enum import Enum
import random
import curses


_SHAPE_MATRICES = dict()
_SHAPE_COLORS = dict()


class TetriminoShape(Enum):
    I = 0
    J = 1
    L = 2
    S = 3
    Z = 4
    T = 5
    O = 6

    @staticmethod
    def get_random():
        return TetriminoShape(random.randrange(len(TetriminoShape)))

    def get_matrix(self):
        return _SHAPE_MATRICES[self]

    def get_color(self):
        return _SHAPE_COLORS[self]

_SHAPE_MATRICES[TetriminoShape.I] = [
    list('XXXX')
]

_SHAPE_MATRICES[TetriminoShape.J] = [
    list('X  '),
    list('XXX')
]

_SHAPE_MATRICES[TetriminoShape.L] = [
    list('  X'),
    list('XXX')
]

_SHAPE_MATRICES[TetriminoShape.S] = [
    list(' XX'),
    list('XX ')
]

_SHAPE_MATRICES[TetriminoShape.Z] = [
    list('XX '),
    list(' XX')
]

_SHAPE_MATRICES[TetriminoShape.T] = [
    list(' X '),
    list('XXX')
]

_SHAPE_MATRICES[TetriminoShape.O] = [
    list('XX'),
    list('XX')
]

_SHAPE_COLORS[TetriminoShape.I] = curses.COLOR_CYAN
_SHAPE_COLORS[TetriminoShape.J] = curses.COLOR_BLUE
_SHAPE_COLORS[TetriminoShape.L] = curses.COLOR_WHITE
_SHAPE_COLORS[TetriminoShape.S] = curses.COLOR_GREEN
_SHAPE_COLORS[TetriminoShape.Z] = curses.COLOR_RED
_SHAPE_COLORS[TetriminoShape.T] = curses.COLOR_MAGENTA
_SHAPE_COLORS[TetriminoShape.O] = curses.COLOR_YELLOW

