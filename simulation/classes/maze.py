from typing import List, Tuple
from simulation.classes.action import Action
from simulation.classes.state import State
from random import randrange


class Maze:
    def __init__(self, states: List[List[State]]) -> None:
        self.states = states

    def calculate_values(self, state: State, discount: float) -> float:
        neighbours = [neighbour[0] for neighbour in self.get_neighbouring_info(self.states, state)]
        new_value = state.calculate_values(neighbours, discount)
        return new_value

    def update_values(self, new_values: List[float]) -> None:
        for row, state_row in enumerate(self.states):
            for col, state in enumerate(state_row):
                state.update_value(new_values[row][col])

    def reset_values(self) -> None:
        self.update_values([[0] * len(self.states)] * len(self.states[0]))

    def generate_episode(self, x: int, y: int, policy) -> List[Tuple[State, Action]]:
        steps = [self.states[y][x]]
        while not self.states[y][x].finish:
            action = policy.get_action(self.states, self.states[y][x])
            if Maze.state_exists(x + action.x, y + action.y):
                x, y = x + action.x, y + action.y
            steps.append(self.states[y][x])
        return steps
    
    def get_random_point(self) -> Tuple[int, int]:
        w, h = len(self.states), len(self.states[0])
        return randrange(w), randrange(h)

    @property
    def total(self):
        return sum(sum(self.states, []))

    @staticmethod
    def get_neighbouring_info(states: List[List[State]], state: State) -> Tuple[State, Action]:
        info = [
            (Maze.get_next_state(states, state, 0, -1), Action.UP),
            (Maze.get_next_state(states, state, 1, 0), Action.RIGHT),
            (Maze.get_next_state(states, state, 0, 1), Action.DOWN),
            (Maze.get_next_state(states, state, -1, 0), Action.LEFT)
        ]
        return info
    
    @staticmethod
    def get_next_state(states: List[List[State]], state: State, x_offset: int, y_offset: int) -> State:
        nx, ny = state.x + x_offset, state.y + y_offset
        return states[ny][nx] if Maze.state_exists(nx, ny) else state

    @staticmethod
    def state_exists(x, y):
        return -1 < x < 4 and -1 < y < 4