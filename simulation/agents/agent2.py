from simulation.agents.base_agent import BaseAgent, conditional_runner
from simulation.classes import Policy
from simulation.classes.tables import RTable


class Agent2(BaseAgent):
    def run(self, visualize: bool = True) -> float:
        r_table = RTable(self.maze.all_states)
        self.policy = Policy(self.maze, Policy.optimal, self.optimal_actions)
        
        total = self.monte_carlo_evaluation(self, r_table)
        if visualize: self.visualize()
        return total
    
    @conditional_runner
    def monte_carlo_evaluation(self, r_table: RTable) -> float:
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        g = 0
        for i in range(len(episode) - 2, -1, -1):
            state, next_state = episode[i], episode[i + 1]
            g = self.discount * g + next_state.reward
            r_table[state] = g
            state.update_value(r_table[state])
        return self.maze.total
