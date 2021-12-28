from dataclasses import dataclass

@dataclass
class ReturnValue:
    average: float = 0
    size: int = 0

    def update_average(self, g: float) -> 'ReturnValue':
        self.size += 1
        self.average += (g - self.average) / self.size
        return self

    @property
    def get(self) -> float:
        return (self.average / self.size) if self.size > 0 else 0

    def __lt__(self, other: 'ReturnValue') -> bool:
        return self.get < other.get