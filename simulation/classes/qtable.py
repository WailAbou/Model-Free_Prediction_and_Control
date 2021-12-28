from typing import Dict, List, Tuple
from simulation.classes.state import State
from simulation.classes.action import Action
from simulation.classes.return_value import ReturnValue


class QTable:
    q_values: Dict[Tuple[State, Action], ReturnValue] = {}
    q_probabilities: Dict[State, Dict[Action, float]] = {}

    def __init__(self, end_states) -> None:
        for end_state in end_states: 
            self.q_probabilities[end_state] = [0, 0, 0, 0]

    @property
    def probabilities(self):
        values = [item[1] for item in sorted(self.q_probabilities.items())]
        parsed_values = [list(self.chunks([all_values[i] for all_values in values], 4)) for i in range(4)]
        return parsed_values

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]
            
    def update_value(self, key: Tuple[State, Action], average: float):
        self.q_values[key] = ReturnValue() if self.q_values.get(key) == None else self.q_values[key].update_average(average)

    def update_probability(self, key: State, index: int, probability: float):
        if key not in self.q_probabilities.keys(): 
            self.q_probabilities[key] = [0, 0, 0, 0]
        self.q_probabilities[key][index] = probability

    def get_a_star_action(self, state: State) -> Action:
        all_returns = [ReturnValue() if self.q_values.get((state, action)) == None else self.q_values[(state, action)] for action in Action.all()]
        a_star_return = max(all_returns)
        return Action.all()[all_returns.index(a_star_return)]
