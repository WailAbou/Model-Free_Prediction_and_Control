from random import choice
from typing import Any, Callable, List, Tuple, Optional
from simulation.classes.action import Action
from simulation.classes.maze import Maze
from simulation.classes.state import State


class Policy:
    def __init__(self, value_function: Callable[[Tuple[State, Action], State], Action], *args: Any) -> None:
        self.value_function = value_function
        self.args = args

    def get_actions(self, states: List[List[State]]) -> List[List[Action]]:
        get_action = lambda state: self.get_action(states, state)
        actions = [list(map(get_action, state_row)) for state_row in states]
        return actions

    def get_action(self, states: List[List[State]], state: State) -> List[Optional[Action]]:
        info_pairs = Maze.get_neighbouring_info(states, state)
        action = self.value_function(info_pairs, state, *self.args)
        return None if state.finish else action

    @staticmethod
    def greedy(info_pairs: Tuple[State, Action], state: State) -> Action:
        totals = list(map(lambda info_pair: info_pair[0].total, info_pairs))
        max_value = max(totals)
        chosen = info_pairs[totals.index(max_value)][1]
        return chosen

    @staticmethod
    def random(info_pairs: Tuple[State, Action], state: State) -> Action:
        return choice(info_pairs)[1]

    @staticmethod
    def optimal(info_pairs: Tuple[State, Action], state: State, actions: List[List[Action]]) -> Action:
        return actions[state.y][state.x]
