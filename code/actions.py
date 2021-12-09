from enum import Enum

class Action(Enum):
    UP = '↑'
    RIGHT = '→'
    DOWN = '↓'
    LEFT = '←'

    @property
    def x(self):
        return action_map[self][0]

    @property
    def y(self):
        return action_map[self][1]

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


action_map = { Action.UP: (0, -1), Action.RIGHT: (1, 0), Action.DOWN: (0, 1), Action.LEFT: (-1, 0) }
