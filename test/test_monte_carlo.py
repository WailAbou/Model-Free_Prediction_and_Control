from unittest import TestCase, main as unittest_main
from simulation.classes import State
from simulation.agents import Agent2, Agent4


class TestDeterministicMonteCarlo(TestCase):
    rewards = [[-1, -1, -1 ,  40], 
               [-1, -1, -10, -10], 
               [-1, -1, -1 , -1 ], 
               [10, -2, -1 , -1 ]]

    def monte_carlo_evaluation(self):
        for discount in [1, 0.9]:
            states = [[State(col, row, self.rewards[row][col]) for col in range(4)] for row in range(4)]
            states[0][3].finish, states[3][0].finish = True, True
            agent = Agent2(2, 3, states, discount=discount)
            end_total = agent.run(False)
            self.assertEqual(end_total, 537)

    def monte_carlo_control(self):
        for discount in [1, 0.9]:
            states = [[State(col, row, self.rewards[row][col]) for col in range(4)] for row in range(4)]
            states[0][3].finish, states[3][0].finish = True, True
            agent = Agent4(2, 3, states, discount=discount)
            end_total = agent.run(False)
            self.assertEqual(end_total, 537)


unittest_main(argv=[''], verbosity=2, exit=False)
