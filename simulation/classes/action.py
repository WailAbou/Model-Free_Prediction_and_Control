from enum import Enum
from typing import List


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

    @staticmethod
    def all() -> List['Action']:
        return [Action.UP, Action.RIGHT, Action.DOWN, Action.LEFT]

    @staticmethod
    def by_state(state, next_state) -> 'Action':
        direction =  next_state - state
        action_index = list(action_map.values()).index(direction)
        return list(action_map.keys())[action_index]

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


action_map = { Action.UP: (0, -1), Action.RIGHT: (1, 0), Action.DOWN: (0, 1), Action.LEFT: (-1, 0) }
