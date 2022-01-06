from typing import Dict, List
from simulation.classes.state import State


class PTable:
    probabilities: Dict[State, List[float]] = {}

    def __init__(self, states: List[State]) -> None:
        for state in states: 
            self.probabilities[state] = [0, 0, 0, 0]

    def __setitem__(self, key: State, value: List[float]) -> None:
        self.probabilities[key] = value
        
    @property
    def get(self):
        values = [item[1] for item in sorted(self.probabilities.items())]
        parsed_values = [list(self.chunks([all_values[i] for all_values in values], 4)) for i in range(4)]
        return parsed_values

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]
