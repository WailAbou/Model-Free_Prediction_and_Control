from simulation.classes import Policy, QTable, Action
from simulation.agents.base_agent import BaseAgent, conditional_runner


class Agent5(BaseAgent):
    epsilon: float = 0.1

    def run(self, visualize: bool = True) -> float:
        self.policy, q_table = Policy(Policy.optimal, self.optimal_actions), QTable(self.maze.end_states)
        total = self.sarsa(self, q_table)
        if visualize: self.visualizer.visualize_table(q_table.chances)
        return total
    
    @conditional_runner
    def sarsa(self, q_table: QTable) -> float:
        return self.maze.total
