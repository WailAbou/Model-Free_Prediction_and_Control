from dataclasses import dataclass
from typing import Dict, Tuple
from simulation.classes.state import State
from simulation.classes.action import Action
from simulation.classes.return_data import Return


@dataclass
class QTable:
    q_values: Dict[Tuple[State, Action], Return]
    q_chances: Dict[State, Dict[Action, float]]

    def update_value(self, key: Tuple[State, Action], g: float):
        self.q_values[key] = Return() if self.q_values.get(key) == None else self.q_values[key].update_average(g)

    def update_chance(self, key: State, index: int, chance: float):
        if key not in self.q_chances.keys(): 
            self.q_chances[key] = [0, 0, 0, 0]
        self.q_chances[key][index] = chance

    def get_a_star_action(self, key: Tuple[State, Action]) -> Action:
        all_returns = [Return() if self.q_values.get(key) == None else self.q_values[key] for action in Action.all()]
        a_star_return = max(all_returns)
        return Action.all()[all_returns.index(a_star_return)]
