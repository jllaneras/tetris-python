from enum import Enum
import curses

class InputAction(Enum):
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    ROTATE = 3
    QUIT = 4

    @staticmethod
    def get_action(character):
        if  character == curses.KEY_LEFT:
            return InputAction.LEFT
        elif character == curses.KEY_DOWN:
            return InputAction.DOWN
        elif character == curses.KEY_RIGHT:
            return InputAction.RIGHT
        elif character in [ord(' '), curses.KEY_UP]:
            return InputAction.ROTATE
        elif character in [ord('q'), ord('Q')]:
            return InputAction.QUIT
        else:
            return None