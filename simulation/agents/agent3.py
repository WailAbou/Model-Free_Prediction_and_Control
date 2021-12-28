from simulation.classes import Maze, Policy
from simulation.agents.base_agent import BaseAgent, conditional_runner


class Agent3(BaseAgent):
    step_size: float = 0.1

    def run(self, visualize: bool = True) -> float:
        self.policy = Policy(Policy.optimal, self.optimal_actions)
        total = self.temporal_difference_learning(self)
        if visualize: self.visualize()
        return total
    
    @conditional_runner
    def temporal_difference_learning(self) -> float:
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        for state in episode:
            action = self.policy.get_action(self.maze.states, state)
            if action == None: break
            next_state = Maze.get_next_state(self.maze.states, state, action)
            new_value = state.value + self.step_size * (next_state.reward + self.discount * (next_state.value - state.value))
            state.update_value(new_value)
        return self.maze.total
