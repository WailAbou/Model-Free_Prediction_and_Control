from os import getcwd as os_getcwd, path as os_path
from sys import path as sys_path
sys_path.append(os_path.join(os_getcwd(), 'code'))

from unittest import TestCase, main as unittest_main
from maze_cell import MazeCell
from agents.agent2 import Agent2
from agents.agent3 import Agent3


class TestDeterministicMonteCarlo(TestCase):
    rewards = [[-1, -1, -1 ,  40], 
               [-1, -1, -10, -10], 
               [-1, -1, -1 , -1 ], 
               [10, -2, -1 , -1 ]]

    def test_random(self):
        for discount, min_total, max_total in [(1, 200, 250), (0.9, 150, 200)]:
            maze_cells = [[MazeCell(col, row, self.rewards[row][col]) for col in range(4)] for row in range(4)]
            maze_cells[0][3].finish, maze_cells[3][0].finish = True, True
            agent = Agent2(2, 3, maze_cells, discount=discount)
            end_total = agent.run(False)
            print(end_total)
            self.assertTrue(min_total <= end_total <= max_total)

    def optimal(self):
        for discount in [1, 0.9]:
            maze_cells = [[MazeCell(col, row, self.rewards[row][col]) for col in range(4)] for row in range(4)]
            maze_cells[0][3].finish, maze_cells[3][0].finish = True, True
            agent = Agent3(2, 3, maze_cells, discount=discount)
            end_total = agent.run(False)
            self.assertEqual(end_total, 537)


unittest_main(argv=[''], verbosity=2, exit=False)
