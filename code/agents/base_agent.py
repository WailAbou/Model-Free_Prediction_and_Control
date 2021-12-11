from abc import abstractmethod
from typing import Any, List, Callable
from actions import Action
from maze_cell import MazeCell
from maze import Maze
from policy import Policy
from visualizer import Visualizer
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
    def __init__(self, x: int, y: int, maze_cells: List[List[MazeCell]], discount: int = 1) -> None:
        self.x, self.y = x, y
        self.maze = Maze(maze_cells)
        self.discount = discount
        self.policy = Policy(Policy.greedy)
        self.visualizer = Visualizer()

    @abstractmethod
    def run(self, print_values: bool=True) -> float:
        raise NotImplementedError()

    def visualize(self):
        actions = self.policy.get_actions(self.maze.maze_cells)
        self.visualizer.print_grids(self.maze.maze_cells, actions)

    @conditional_runner
    def value_iteration(self, discount: float) -> float:
        """Updates the state of the maze by updating all the maze cells.

        Parameters
        ----------
        discount
            A discount value for the bellman_equation.

        Returns
        -------
        float
            The total sum of all the maze cells value.
        """
        calculate_values = lambda maze_cell: self.maze.calculate_values(maze_cell, discount)
        new_values = [list(map(calculate_values, row_cells)) for row_cells in self.maze.maze_cells]
        self.maze.update_values(new_values)
        return self.maze.total
