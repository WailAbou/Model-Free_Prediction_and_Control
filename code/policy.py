from random import choice
from typing import Any, Callable, List, Tuple, Optional
from actions import Action
from maze import Maze
from maze_cell import MazeCell


class Policy:
    def __init__(self, value_function: Callable[[Tuple[MazeCell, Action], MazeCell], Action], *args: Any) -> None:
        self.value_function = value_function
        self.args = args

    def get_actions(self, maze_cells: List[List[MazeCell]]) -> List[List[Action]]:
        get_action = lambda maze_cell: self.get_action(maze_cells, maze_cell)
        actions = [list(map(get_action, maze_row)) for maze_row in maze_cells]
        return actions

    def get_action(self, maze_cells: List[List[MazeCell]], maze_cell: MazeCell) -> List[Optional[Action]]:
        info_pairs = Maze.get_neighbouring_info(maze_cells, maze_cell)
        action = self.value_function(info_pairs, maze_cell, *self.args)
        return None if maze_cell.finish else action

    @staticmethod
    def greedy(info_pairs: Tuple[MazeCell, Action], maze_cell: MazeCell) -> Action:
        totals = list(map(lambda info_pair: info_pair[0].total, info_pairs))
        max_value = max(totals)
        chosen = info_pairs[totals.index(max_value)][1]
        return chosen

    @staticmethod
    def random(info_pairs: Tuple[MazeCell, Action], maze_cell: MazeCell) -> Action:
        return choice(info_pairs)[1]

    @staticmethod
    def optimal(info_pairs: Tuple[MazeCell, Action], maze_cell: MazeCell, actions: List[List[Action]]) -> Action:
        return actions[maze_cell.y][maze_cell.x]
