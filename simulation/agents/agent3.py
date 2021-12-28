from simulation.classes import Maze, Policy
from simulation.agents.base_agent import BaseAgent, conditional_runner


class Agent3(BaseAgent):
    def run(self, print_values: bool = True) -> float:
        self.policy = Policy(Policy.optimal, self.optimal_actions)
        total = self.temporal_difference_learning(self)
        if print_values: self.visualize()
        return total
    
    @conditional_runner
    def temporal_difference_learning(self) -> float:
        step_size = 0.1
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        for state in episode:
            action = self.policy.get_action(self.maze.states, state)
            if action == None: break
            next_state = Maze.get_next_state(self.maze.states, state, action)
            new_value = state.value + step_size * (next_state.reward + self.discount * (next_state.value - state.value))
            state.update_value(new_value)
        return self.maze.total
