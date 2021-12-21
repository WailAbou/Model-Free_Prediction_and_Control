from simulation.agents.base_agent import BaseAgent


class Agent1(BaseAgent):
    def run(self, print_values: bool = True) -> float:
        total = self.value_iteration(self)
        if print_values: self.visualize()
        return total
