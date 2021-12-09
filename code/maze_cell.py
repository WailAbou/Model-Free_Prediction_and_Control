from dataclasses import dataclass
from typing import List


@dataclass
class MazeCell:
    x: int = -1
    y: int = -1
    reward: float = 0
    chance: float = 1
    value: float = 0
    finish: bool = False

    @property
    def total(self) -> float:
        return self.reward + self.value

    def update_value(self, new_value: float) -> None:
        if not self.finish:
            self.value = new_value #: updates the current value with the newly calculated value if not the finish cell

    def calculate_values(self, neighbours: List['MazeCell'], discount: float) -> float:
        """Calculate the new value of this maze cell.

        Parameters
        ----------
        neighbours
            The neighbours of this cell.
        discount
            A discount value for the bellman_equation.

        Returns
        -------
        float
            The newly calculated value.
        """
        if self.finish: return self.value #: if this is the end cell don't waste time calculating the value
        elif self.chance == 1: return max([self.bellman_equation(neighbour, discount, self.chance) for neighbour in neighbours]) #: deterministic
        else: return self.calculate_chances(neighbours, discount) #: not deterministic

    def calculate_chances(self, neighbours: List['MazeCell'], discount: float) -> float:
        """Calculate the new value of this maze cell based on the chances.

        Parameters
        ----------
        neighbours
            The neighbours of this cell.
        discount
            A discount value for the bellman_equation.

        Returns
        -------
        float
            The newly calculated value.
        """
        remainder_chance = (1 - self.chance) / 3
        combo = [self.chance, remainder_chance, remainder_chance, remainder_chance]
        chances_combos = [[combo[i%4], combo[(i+1)%4], combo[(i+2)%4], combo[(i+3)%4]] for i in range(len(combo))]
        new_values = [sum([self.bellman_equation(neighbours[i], discount, chance) for i, chance in enumerate(chances)]) for chances in chances_combos]
        return max(new_values)

    def bellman_equation(self, neighbour: 'MazeCell', discount: float, chance: float) -> float:
        """Calculate the new value of this maze cell.

        Parameters
        ----------
        neighbour
            The neighbours of this cell.
        discount
            A discount value for the bellman_equation.
        chance
            The chance the action will succeeded

        Returns
        -------
        float
            The newly calculated value.
        """
        return chance * (neighbour.reward + (discount * neighbour.value))

    def __str__(self) -> str:
        # return f"({self.x}, {self.y})"
        return f"R:{self.reward:.2f} & V:{self.value:.2f}"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
        return f"R:{self.reward:.2f} & V:{self.value:.2f}"

    def __hash__(self) -> int:
        return self.x + self.y

    def __radd__(self, other: int) -> int:
        return self.total + other