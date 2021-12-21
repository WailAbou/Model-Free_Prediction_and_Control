from typing import Dict
from simulation.agents.base_agent import BaseAgent, conditional_runner
from simulation.classes import Return, Policy, State
from collections import OrderedDict


class Agent2(BaseAgent):
    def run(self, print_values: bool = True) -> float:
        self.policy, returns = Policy(Policy.optimal, self.optimal_actions), {}
        total = self.monte_carlo_evaluation(self, returns)
        if print_values: self.visualize()
        return total
    
    @conditional_runner
    def monte_carlo_evaluation(self, returns: Dict[State, Return]) -> float:
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        first_visit_episode = list(OrderedDict.fromkeys(episode))
        g = 0
        for i in range(len(first_visit_episode) - 2, -1, -1):
            step = first_visit_episode[i]
            g = self.discount * g + first_visit_episode[i + 1].reward
            returns[step] = Return() if returns.get(step) == None else returns[step].update_average(g)
            step.update_value(returns[step].average)
        return self.maze.total
