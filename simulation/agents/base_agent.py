from abc import abstractmethod
from typing import Any, List, Callable
from simulation.classes import Maze, State, Policy
from simulation.graphical.visualizer import Visualizer
from tqdm import tqdm


class conditional_runner(object):
    def __init__(self, algorithm: Callable[[Any], float]):
        self.algorithm = algorithm

    def __call__(self, caller_source, *args):
        old_total, total, delta, iterations = 0, 1, 0.01, 0
        min_iterations, max_iterations = 1e4, 1e6
        pbar = tqdm(total=min_iterations)
        while (iterations < min_iterations or abs(total - old_total) > delta) and iterations < max_iterations:
            old_total, total = total, self.algorithm(caller_source, *args)
            iterations += 1
            pbar.update()
        pbar.close()
        return total


class BaseAgent:
    def __init__(self, x: int, y: int, states: List[List[State]], discount: int = 1) -> None:
        self.x, self.y = x, y
        self.discount = discount
        self.maze = Maze(states)
        self.policy = Policy(Policy.greedy)
        self.visualizer = Visualizer()

    @abstractmethod
    def run(self, visualize: bool = True) -> float:
        raise NotImplementedError()

    def visualize(self):
        actions = self.policy.get_actions(self.maze.states)
        self.visualizer.visualize_text(self.maze.states, actions)

    @conditional_runner
    def value_iteration(self) -> float:
        calculate_values = lambda state: self.maze.calculate_values(state, self.discount)
        new_values = [list(map(calculate_values, row_states)) for row_states in self.maze.states]
        self.maze.update_values(new_values)
        return self.maze.total

    @property
    def optimal_actions(self):
        self.value_iteration(self)
        actions = self.policy.get_actions(self.maze.states)
        self.maze.reset_values()
        return actions
