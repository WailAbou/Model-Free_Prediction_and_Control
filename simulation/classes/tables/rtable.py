from typing import Dict, List, Any
from simulation.classes.return_value import ReturnValue
from itertools import product

class RTable:
    r_values: Dict[Any, ReturnValue] = {}

    def __init__(self, *targets: List[List[Any]]) -> None:
        keys = [item[0] if len(item) == 1 else item for item in product(*targets)]
        for key in keys: 
            self.r_values[key] = ReturnValue()

    def __getitem__(self, key: Any) -> ReturnValue:
        return self.r_values[key].average

    def __setitem__(self, key: Any, value: float) -> None:
        self.r_values[key].update_average(value)