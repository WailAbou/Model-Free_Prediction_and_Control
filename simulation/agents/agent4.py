from simulation.classes import Policy, Action
from simulation.agents.base_agent import BaseAgent, conditional_runner
from simulation.classes.tables import RTable, QTable, PTable


class Agent4(BaseAgent):
    epsilon: float = 0.1
    
    def run(self, visualize: bool = True) -> float:
        p_table = PTable(self.maze.all_states)
        q_table = QTable(self.maze.all_states, Action.all())
        r_table = RTable(self.maze.all_states, Action.all())
        self.policy = Policy(self.maze, Policy.optimal, self.optimal_actions)
        
        total = self.monte_carlo_control(self, r_table, q_table, p_table)
        if visualize: 
            self.visualizer.visualize_table(q_table.get)
            self.visualizer.visualize_table(p_table.get)
        return total
    
    @conditional_runner
    def monte_carlo_control(self, r_table: RTable, q_table: QTable, p_table: PTable) -> float:
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        g = 0
        for i in range(len(episode) - 2, -1, -1):
            state, next_state = episode[i], episode[i + 1]
            g = self.discount * g + next_state.reward
            action = Action.by_state(state, next_state)

            r_table[(state, action)] = g
            q_table[(state, action)] = r_table[(state, action)]

            a_star_action = q_table.get_a_star_action(state)
            calculate_probability = lambda action: 1 - self.epsilon + self.epsilon / len(Action.all()) if action == a_star_action else self.epsilon / len(Action.all())
            p_table[state] = [calculate_probability(action) for action in Action.all()]
        return self.maze.total
