from os import getcwd as os_getcwd, path as os_path
from sys import path as sys_path
sys_path.append(os_path.join(os_getcwd(), 'code'))

from unittest import TestCase, main as unittest_main
from maze_cell import MazeCell
from agents.agent1 import Agent1

class TestDeterministicMdp(TestCase):
    def test_maze(self):
        rewards = [[-1, -1, -1 ,  40], 
                   [-1, -1, -10, -10], 
                   [-1, -1, -1 , -1 ], 
                   [10, -2, -1 , -1 ]]
        maze_cells = [[MazeCell(col, row, rewards[row][col]) for col in range(4)] for row in range(4)]
        maze_cells[0][3].finish, maze_cells[3][0].finish = True, True
        agent = Agent1(2, 3, maze_cells)
        end_total = agent.run(False)
        self.assertEqual(end_total, 537)


unittest_main(argv=[''], verbosity=2, exit=False)
