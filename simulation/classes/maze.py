from typing import List, Tuple
from simulation.classes.action import Action
from simulation.classes.state import State
from random import randrange
from collections import OrderedDict


class Maze:
    def __init__(self, states: List[List[State]]) -> None:
        self.states = states

    def calculate_values(self, state: State, discount: float) -> float:
        neighbours = self.get_neighbouring_states(self.states, state)
        new_value = state.calculate_values(neighbours, discount)
        return new_value

    def update_values(self, new_values: List[float]) -> None:
        for row, state_row in enumerate(self.states):
            for col, state in enumerate(state_row):
                state.update_value(new_values[row][col])

    def reset_values(self) -> None:
        self.update_values([[0] * len(self.states)] * len(self.states[0]))

    def generate_episode(self, x: int, y: int, policy, first_visit: bool = True) -> List[Tuple[State, Action]]:
        state = self.states[y][x]
        episode = [state]
        while not state.finish:
            action = policy.get_action(self.states, state)
            state = self.take_step(state, action)
            episode.append(state)
        return list(OrderedDict.fromkeys(episode)) if first_visit else episode
    
    def take_step(self, state, action):
        new_x, new_y = state.x + action.x, state.y + action.y
        if Maze.state_exists(new_x, new_y):
            return self.states[new_y][new_x]
        return state

    def get_random_point(self) -> Tuple[int, int]:
        w, h = len(self.states), len(self.states[0])
        return randrange(w), randrange(h)

    @property
    def end_states(self):
        return [state for state in sum(self.states, []) if state.finish]

    @property
    def total(self):
        return sum(sum(self.states, []))

    @staticmethod
    def get_neighbouring_states(states: List[List[State]], state: State) -> List[State]:
        states = [
            Maze.get_next_state(states, state, Action.UP), Maze.get_next_state(states, state, Action.RIGHT), 
            Maze.get_next_state(states, state, Action.DOWN), Maze.get_next_state(states, state, Action.LEFT)
        ]
        return states
    
    @staticmethod
    def get_next_state(states: List[List[State]], state: State, action: Action) -> State:
        nx, ny = state.x + action.x, state.y + action.y
        return states[ny][nx] if Maze.state_exists(nx, ny) else state

    @staticmethod
    def state_exists(x, y):
        return -1 < x < 4 and -1 < y < 4