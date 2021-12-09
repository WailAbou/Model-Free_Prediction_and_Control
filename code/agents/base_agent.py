from abc import abstractmethod
from typing import Any, List, Callable, Tuple
from actions import Action
from maze_cell import MazeCell
from maze import Maze
from policy import Policy
from visualizer import Visualizer


class BaseAgent:
    def __init__(self, x: int, y: int, maze_cells: List[List[MazeCell]], discount: int = 1) -> None:
        self.x, self.y = x, y
        self.maze = Maze(maze_cells)
        self.discount = discount
        self.policy = Policy(Policy.greedy)
        self.visualizer = Visualizer()

    @abstractmethod
    def run(self, print_values: bool=True) -> float:
        raise NotImplementedError()

    def conditional_runner(self, algorithm: Callable[[Any], None], min_iterations: int = 1e4, max_iterations: int = 1e6, *args: Any) -> float:
        old_total, total, delta, iterations = 0, 1, 0.01, 0
        while (iterations < min_iterations or abs(total - old_total) > delta) and iterations < max_iterations:
            algorithm(*args)
            old_total, total = total, self.maze.total
            iterations += 1
        return total

    def visualize(self, actions: List[Action] = None):
        actions = actions or self.policy.get_actions(self.maze.maze_cells)
        self.visualizer.print_grids(self.maze.maze_cells)
