from random import random
from maze import Maze
from policy import Policy
from agents.base_agent import BaseAgent, conditional_runner


class Agent4(BaseAgent):
    def run(self, print_values: bool = True) -> float:
        self.value_iteration(self, self.discount)
        actions = self.policy.get_actions(self.maze.maze_cells)
        self.maze.reset_values()

        self.policy = Policy(Policy.optimal, actions)
        total = self.temporal_difference_learning(self)
        
        if print_values: self.visualize()
        return total
    
    @conditional_runner
    def temporal_difference_learning(self) -> float:
        episode = self.maze.generate_episode(*self.maze.get_random_point(), self.policy)
        for step in episode:
            action = self.policy.get_action(self.maze.maze_cells, step)
            if action == None: break

            next_cell = Maze.get_cell(self.maze.maze_cells, step, action.x, action.y)
            new_value = step.value + 0.9 * (next_cell.reward + self.discount * (next_cell.value - step.value))
            step.update_value(new_value)
        return self.maze.total
