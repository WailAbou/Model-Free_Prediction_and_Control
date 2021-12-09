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
        algorithm = lambda: self.value_iteration(self.discount)
        total = self.conditional_runner(algorithm)
        if print_values: self.visualize()
        return total

    def value_iteration(self, discount: float) -> float:
        """Updates the state of the maze by updating all the maze cells.

        Parameters
        ----------
        discount
            A discount value for the bellman_equation.

        Returns
        -------
        float
            The total sum of all the maze cells value.
        """
        calculate_values = lambda maze_cell: self.maze.calculate_values(maze_cell, discount)
        new_values = [list(map(calculate_values, row_cells)) for row_cells in self.maze.maze_cells]
        self.maze.update_values(new_values)