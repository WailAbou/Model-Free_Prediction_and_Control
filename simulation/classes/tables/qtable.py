from typing import Dict, List, Tuple
from simulation.classes.state import State
from simulation.classes.action import Action


class QTable:
    values: Dict[Tuple[State, Action], float] = {}

    def __init__(self, states: List[State], actions: List[Action]) -> None:
        for state in states:
            for action in actions:
                self.values[(state, action)] = 0

    def __getitem__(self, key: Tuple[State, Action]) -> float:
        return self.values[key]

    def __setitem__(self, key: Tuple[State, Action], value: float) -> None:
        self.values[key] = value

    @property
    def get(self):
        values = [item[1] for item in sorted(self.values.items(), key=lambda x: x[0][0])]
        values = list(self.chunks(values, 4))
        parsed_values = [list(self.chunks([all_values[i] for all_values in values], 4)) for i in range(4)]
        return parsed_values

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]
            
    def get_a_star_action(self, state: State) -> Action:
        all_state_values = [self.values[(state, action)] for action in Action.all()]
        a_star_value = max(all_state_values)
        a_star_action = Action.all()[all_state_values.index(a_star_value)]
        return a_star_action
