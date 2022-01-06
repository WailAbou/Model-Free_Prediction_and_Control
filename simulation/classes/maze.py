from typing import List, Tuple
from simulation.classes.action import Action
from simulation.classes.state import State
from random import randrange
from collections import OrderedDict


class Maze:
    def __init__(self, states: List[List[State]]) -> None:
        self.states = states

    @property
    def all_states(self):
        return [state for state in sum(self.states, [])]

    @property
    def end_states(self):
        return [state for state in sum(self.states, []) if state.finish]

    @property
    def total(self):
        return sum(sum(self.states, []))

    def calculate_value(self, state: State, discount: float) -> float:
        neighbours = self.get_neighbours(state)
        new_value = state.calculate_value(neighbours, discount)
        return new_value

    def update_values(self, new_values: List[float]) -> None:
        for row, state_row in enumerate(self.states):
            for col, state in enumerate(state_row):
                state.update_value(new_values[row][col])

    def reset_values(self) -> None:
        self.update_values([[0] * len(self.states)] * len(self.states[0]))

    def generate_episode(self, x: int, y: int, policy, first_visit: bool = True) -> List[State]:
        state = self.states[y][x]
        episode = [state]
        while not state.finish:
            action = policy.get_action(state)
            state = self.step(state, action)
            episode.append(state)
        return list(OrderedDict.fromkeys(episode)) if first_visit else episode
    
    def step(self, state: State, action: Action) -> State:
        nx, ny = state.x + action.x, state.y + action.y
        return self.states[ny][nx] if Maze.state_exists(nx, ny) else state

    def get_random_point(self) -> Tuple[int, int]:
        w, h = len(self.states), len(self.states[0])
        return randrange(w), randrange(h)

    def get_neighbours(self, state: State) -> List[State]:
        states = [
            self.step(state, Action.UP), self.step(state, Action.RIGHT), 
            self.step(state, Action.DOWN), self.step(state, Action.LEFT)
        ]
        return states

    @staticmethod
    def state_exists(x, y):
        return -1 < x < 4 and -1 < y < 4