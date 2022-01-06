from random import choice
from typing import Any, Callable, List, Tuple, Optional
from simulation.classes.action import Action
from simulation.classes.maze import Maze
from simulation.classes.state import State
from simulation.classes.tables import QTable


class Policy:
    def __init__(self, maze: Maze, value_function: Callable[[Tuple[State, Action], State], Action], *args: Any) -> None:
        self.maze = maze
        self.value_function = value_function
        self.args = args

    def get_actions(self, states: List[List[State]]) -> List[List[Optional[Action]]]:
        actions = [list(map(self.get_action, state_row)) for state_row in states]
        return actions

    def get_action(self, state: State) -> Optional[Action]:
        neighbours = self.maze.get_neighbours(state)
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

    @staticmethod
    def epsilon_greedy(neighbours: List[State], state: State, q_table: QTable) -> Action:
        return q_table.get_a_star_action(state)
