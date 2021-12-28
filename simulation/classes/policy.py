from random import choice
from typing import Any, Callable, List, Tuple, Optional
from simulation.classes.action import Action
from simulation.classes.maze import Maze
from simulation.classes.state import State


class Policy:
    def __init__(self, value_function: Callable[[Tuple[State, Action], State], Action], *args: Any) -> None:
        self.value_function = value_function
        self.args = args

    def get_actions(self, states: List[List[State]]) -> List[List[Optional[Action]]]:
        get_action = lambda state: self.get_action(states, state)
        actions = [list(map(get_action, state_row)) for state_row in states]
        return actions

    def get_action(self, states: List[List[State]], state: State) -> Optional[Action]:
        neighbours = Maze.get_neighbouring_states(states, state)
        action = self.value_function(neighbours, state, *self.args)
        return None if state.finish else action

    @staticmethod
    def greedy(neighbours: List[State], state: State) -> Action:
        totals = list(map(lambda neighbour: neighbour.total, neighbours))
        max_value = max(totals)
        chosen = totals.index(max_value)
        return Action.all()[chosen]

    @staticmethod
    def random(neighbours: List[State], state: State) -> Action:
        return choice(Action.all())

    @staticmethod
    def optimal(neighbours: List[State], state: State, actions: List[List[Action]]) -> Action:
        return actions[state.y][state.x]
