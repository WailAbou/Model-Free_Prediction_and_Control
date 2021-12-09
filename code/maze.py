from typing import List, Tuple
from actions import Action
from maze_cell import MazeCell
from random import randrange

class Maze:
    def __init__(self, maze_cells: List[List[MazeCell]]) -> None:
        self.maze_cells = maze_cells

    def calculate_values(self, maze_cell: MazeCell, discount: float) -> float:
        """Calculates the new value of the given maze cell.

        Parameters
        ----------
        maze_cell
            The current maze cell to calculate the values of
        discount
            A discount value for the bellman_equation.

        Returns
        -------
        float
            The new calculated value.
        """
        neighbours = [neighbour[0] for neighbour in self.get_neighbouring_info(self.maze_cells, maze_cell)]
        new_value = maze_cell.calculate_values(neighbours, discount)
        return new_value

    def update_values(self, new_values: List[float]) -> None:
        for row, maze_row in enumerate(self.maze_cells):
            for col, maze_cell in enumerate(maze_row):
                maze_cell.update_value(new_values[row][col])

    def reset_values(self) -> None:
        self.update_values([[0] * len(self.maze_cells)] * len(self.maze_cells[0]))

    def generate_episode(self, x: int, y: int, policy):
        steps = [self.maze_cells[y][x]]
        while not self.maze_cells[y][x].finish:
            action = policy.get_action(self.maze_cells, self.maze_cells[y][x])
            if Maze.maze_cell_exists(x + action.x, y + action.y):
                x, y = x + action.x, y + action.y
            steps.append(self.maze_cells[y][x])
        return steps

    
    def get_random_point(self):
        w, h = len(self.maze_cells), len(self.maze_cells[0])
        return (randrange(w), randrange(h))

    @property
    def total(self):
        return sum(sum(self.maze_cells, []))

    @staticmethod
    def get_neighbouring_info(maze_cells: List[List[MazeCell]], maze_cell: MazeCell) -> Tuple[MazeCell, Action]:
        info = [
            (Maze.get_cell(maze_cells, maze_cell, 0, -1), Action.UP),
            (Maze.get_cell(maze_cells, maze_cell, 1, 0), Action.RIGHT),
            (Maze.get_cell(maze_cells, maze_cell, 0, 1), Action.DOWN),
            (Maze.get_cell(maze_cells, maze_cell, -1, 0), Action.LEFT)
        ]
        return info
    
    @staticmethod
    def get_cell(maze_cells: List[List[MazeCell]], maze_cell: MazeCell, x_offset: int, y_offset: int) -> MazeCell:
        """Gets a cell given a list of all cells the current cell and the x and y offsets.

        Parameters
        ----------
        maze_cell
            The current maze cell to calculate the values of
        discount
            A discount value for the bellman_equation.

        Returns
        -------
        MazeCell
            The found maze cell (the given maze cell if it is not found).
        """
        nx, ny = maze_cell.x + x_offset, maze_cell.y + y_offset
        return maze_cells[ny][nx] if Maze.maze_cell_exists(nx, ny) else maze_cell 

    @staticmethod
    def maze_cell_exists(x, y):
        return -1 < x < 4 and -1 < y < 4