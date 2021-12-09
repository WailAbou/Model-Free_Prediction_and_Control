from dataclasses import dataclass

@dataclass
class Return:
    average: float = 0
    size: int = 0

    def update_average(self, g: float) -> 'Return':
        self.size += 1
        self.average += (g - self.average) / self.size
        return self