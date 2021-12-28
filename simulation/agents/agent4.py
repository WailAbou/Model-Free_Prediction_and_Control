from typing import Dict
from simulation.classes import Policy, QTable, Action, ReturnValue, State
from simulation.agents.base_agent import BaseAgent, conditional_runner


class Agent4(BaseAgent):
    def run(self, print_values: bool = True) -> float:
        self.policy, q_table, returns = Policy(Policy.optimal, self.optimal_actions), QTable(self.maze.end_states), {}
        total = self.monte_carlo_control(self, q_table, returns)
        if print_values: self.visualizer.visualize_table(q_table.probabilities)
        return total
    
    @conditional_runner
    def monte_carlo_control(self, q_table: QTable, returns: Dict[State, ReturnValue]) -> float:
        epsilon = 0.1
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        g = 0
        for i in range(len(episode) - 2, -1, -1):
            step, next_step = episode[i], episode[i + 1]
            g = self.discount * g + next_step.reward
            returns[step] = ReturnValue() if returns.get(step) == None else returns[step].update_average(g)

            action = Action.by_state(step, next_step)
            q_table.update_value((step, action), returns[step].average)
            a_star_action = q_table.get_a_star_action((step, action))

            for i, action in enumerate(Action.all()):
                q_table_probability = 1 - epsilon + epsilon / len(Action.all()) if action == a_star_action else epsilon / len(Action.all())
                q_table.update_probability(step, i, q_table_probability)

        return self.maze.total
