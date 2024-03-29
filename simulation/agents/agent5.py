from simulation.classes import Policy, Action
from simulation.agents.base_agent import BaseAgent, conditional_runner
from simulation.classes.tables import QTable


class Agent5(BaseAgent):
    alpha: float = 0.1

    def run(self, visualize: bool = True) -> float:
        q_table = QTable(self.maze.all_states, Action.all())
        self.policy = Policy(self.maze, Policy.epsilon_greedy, q_table)

        total = self.sarsa(self, q_table)
        if visualize: self.visualizer.visualize_table(q_table.get)
        return total
    
    @conditional_runner
    def sarsa(self, q_table: QTable) -> float:
        x, y = self.maze.get_random_point()
        state = self.maze.states[y][x]
        action = self.policy.get_action(state)
        while not state.finish:
            next_state = self.maze.step(state, action)
            next_action = self.policy.get_action(next_state)
            if next_action == None: break

            q_table[(state, action)] = q_table[(state, action)] + self.alpha * (next_state.reward + self.discount * q_table[(next_state, next_action)] -  q_table[(state, action)])
            state, action = next_state, next_action
        return self.maze.total
