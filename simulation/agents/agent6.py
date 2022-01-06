from simulation.classes import Policy, Action
from simulation.agents.base_agent import BaseAgent, conditional_runner
from simulation.classes.tables import QTable


class Agent6(BaseAgent):
    alpha: float = 0.1

    def run(self, visualize: bool = True) -> float:
        q_table = QTable(self.maze.all_states, Action.all())
        self.policy = Policy(self.maze, Policy.epsilon_greedy, q_table)

        total = self.q_learning(self, q_table)
        if visualize: self.visualizer.visualize_table(q_table.get)
        return total
    
    @conditional_runner
    def q_learning(self, q_table: QTable) -> float:
        x, y = self.maze.get_random_point()
        state = self.maze.states[y][x]
        while not state.finish:
            action = self.policy.get_action(state)
            next_state = self.maze.step(state, action)

            max_q = max([q_table[(next_state, action)] for action in Action.all()])
            q_table[(state, action)] = q_table[(state, action)] + self.alpha * (next_state.reward + self.discount * max_q -  q_table[(state, action)])
            state = next_state
        return self.maze.total
