from simulation.classes import State
from simulation.agents import Agent1, Agent2, Agent3, Agent4, Agent5, Agent6


rewards = [[-1, -1, -1 ,  40], 
           [-1, -1, -10, -10], 
           [-1, -1, -1 , -1 ], 
           [10, -2, -1 , -1 ]]
states = [[State(col, row, rewards[row][col]) for col in range(4)] for row in range(4)]
states[0][3].finish, states[3][0].finish = True, True

# agent = Agent1(2, 3, states)
# agent = Agent2(2, 3, states)
# agent = Agent3(2, 3, states)
# agent = Agent4(2, 3, states)
# agent = Agent5(2, 3, states)
agent = Agent6(2, 3, states)
agent.run()
