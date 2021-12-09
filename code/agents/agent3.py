from agents.agent2 import Agent2
from policy import Policy


class Agent3(Agent2):
    def run(self, print_values: bool = True) -> float:
        algorithm1 = lambda: self.value_iteration(self.discount)
        self.conditional_runner(algorithm1)
        actions = self.policy.get_actions(self.maze.maze_cells)
        self.maze.reset_values()

        algorithm2 = lambda returns: self.monte_carlo_prediction(returns)
        self.policy, returns = Policy(Policy.optimal, actions), {}
        total = self.conditional_runner(algorithm2, 1e4, 1e6, returns)
        if print_values: self.visualize(actions)
        return total
