from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class State:
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
            self.value = new_value

    def calculate_value(self, neighbours: List['State'], discount: float) -> float:
        if self.finish: return self.value
        elif self.chance == 1: return max([self.bellman_equation(neighbour, discount, self.chance) for neighbour in neighbours])
        else: return self.calculate_chance(neighbours, discount)

    def calculate_chance(self, neighbours: List['State'], discount: float) -> float:
        remainder_chance = (1 - self.chance) / 3
        combo = [self.chance, remainder_chance, remainder_chance, remainder_chance]
        chances_combos = [[combo[i%4], combo[(i+1)%4], combo[(i+2)%4], combo[(i+3)%4]] for i in range(len(combo))]
        new_values = [sum([self.bellman_equation(neighbours[i], discount, chance) for i, chance in enumerate(chances)]) for chances in chances_combos]
        return max(new_values)

    def bellman_equation(self, neighbour: 'State', discount: float, chance: float) -> float:
        return chance * (neighbour.reward + (discount * neighbour.value))

    def __str__(self) -> str:
        return f"R:{self.reward:.2f} & V:{self.value:.2f}"

    def __repr__(self) -> str:
        return f"R:{self.reward:.2f} & V:{self.value:.2f}"

    def __hash__(self) -> int:
        return self.x * self.y + self.x + self.y

    def __radd__(self, other: int) -> int:
        return self.total + other

    def __sub__(self, other: 'State') -> Tuple[int, int]:
        return (self.x - other.x, self.y - other.y)

    def __lt__(self, other: 'State') -> bool:
        return (self.y + self.x  * 4) < (other.y + other.x  * 4)
