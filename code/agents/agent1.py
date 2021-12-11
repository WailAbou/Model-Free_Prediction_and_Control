from agents.base_agent import BaseAgent

class Agent1(BaseAgent):
    def run(self, print_values: bool = True) -> float:
        """Excutes value iteration with chosen policy and visualizes it 
        until the difference is smaller then delta.

        Returns
        -------
        new_total
            The last iteration total value of the maze.
        """
        total = self.value_iteration(self, self.discount)
        
        if print_values: self.visualize()
        return total