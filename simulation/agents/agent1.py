from simulation.agents.base_agent import BaseAgent


class Agent1(BaseAgent):
    def run(self, visualize: bool = True) -> float:
        total = self.value_iteration(self)
        if visualize: self.visualize()
        return total
