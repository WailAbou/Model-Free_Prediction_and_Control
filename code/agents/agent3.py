from agents.agent2 import Agent2
from policy import Policy


class Agent3(Agent2):
    def run(self, print_values: bool = True) -> float:
        self.value_iteration(self, self.discount)
        actions = self.policy.get_actions(self.maze.maze_cells)
        self.maze.reset_values()

        self.policy, returns = Policy(Policy.optimal, actions), {}
        total = self.monte_carlo_evaluation(self, returns)
        
        if print_values: self.visualize()
        return total
