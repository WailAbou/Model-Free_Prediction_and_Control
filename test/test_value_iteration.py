from unittest import TestCase, main as unittest_main
from simulation.classes import State
from simulation.agents import Agent1


class TestValueIteration(TestCase):
    def test_deterministic(self):
        rewards = [[-1, -1, -1 ,  40], 
                   [-1, -1, -10, -10], 
                   [-1, -1, -1 , -1 ], 
                   [10, -2, -1 , -1 ]]
        states = [[State(col, row, rewards[row][col]) for col in range(4)] for row in range(4)]
        states[0][3].finish, states[3][0].finish = True, True
        agent = Agent1(2, 3, states)
        end_total = agent.run(False)
        self.assertEqual(end_total, 537)

    def test_non_deterministic(self):
        rewards = [[-1 , -1 , -1 ,  40], 
                   [-1 , -1 , -10, -10], 
                   [-1 , -1 , -1 , -1 ], 
                   [10 , -2 , -1 , -1 ]]
        chances = [[0.1, 0.1, 0.1,  1 ],
                   [ 1 ,  1 ,  1 ,  1 ],
                   [ 1 ,  1 ,  1 ,  1 ],
                   [ 1 ,  1 ,  1 ,  1 ]]
        states = [[State(col, row, rewards[row][col], chances[row][col]) for col in range(4)] for row in range(4)]
        states[0][3].finish, states[3][0].finish = True, True
        agent = Agent1(2, 3, states)
        end_total = agent.run(False)
        self.assertAlmostEqual(end_total, 420, 0)


unittest_main(argv=[''], verbosity=2, exit=False)
