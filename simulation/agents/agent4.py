from typing import Dict, Tuple
from simulation.classes import Policy, QTable, Action, ReturnValue, State
from simulation.agents.base_agent import BaseAgent, conditional_runner


class Agent4(BaseAgent):
    epsilon: float = 0.1
    
    def run(self, visualize: bool = True) -> float:
        self.policy, q_table, returns = Policy(Policy.optimal, self.optimal_actions), QTable(self.maze.end_states), {}
        total = self.monte_carlo_control(self, q_table, returns)
        if visualize: self.visualizer.visualize_table(q_table.probabilities)
        return total
    
    @conditional_runner
    def monte_carlo_control(self, q_table: QTable, returns: Dict[Tuple[State, Action], ReturnValue]) -> float:
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        g = 0
        for i in range(len(episode) - 2, -1, -1):
            state, next_state = episode[i], episode[i + 1]
            g = self.discount * g + next_state.reward
            action = Action.by_state(state, next_state)
            returns[(state, action)] = ReturnValue() if returns.get((state, action)) == None else returns[(state, action)].update_average(g)
            
            q_table.update_value((state, action), returns[(state, action)].average)
            a_star_action = q_table.get_a_star_action(state)

            for i, action in enumerate(Action.all()):
                q_table_probability = 1 - self.epsilon + self.epsilon / len(Action.all()) if action == a_star_action else self.epsilon / len(Action.all())
                q_table.update_probability(state, i, q_table_probability)
        return self.maze.total
