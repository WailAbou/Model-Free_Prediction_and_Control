from dataclasses import dataclass

@dataclass
class ReturnValue:
    average: float = 0
    size: int = 0

    def update_average(self, g: float) -> 'ReturnValue':
        self.size += 1
        self.average += (g - self.average) / self.size
        return self

    def __lt__(self, other: 'ReturnValue') -> bool:
        return self.average < other.average

    def __sub__(self, other: 'ReturnValue') -> float:
        return self.average - other.average