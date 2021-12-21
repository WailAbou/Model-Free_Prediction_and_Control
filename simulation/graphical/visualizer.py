from typing import Any, List
from simulation.graphical.text_graphic import TextGraphic
from simulation.graphical.table_graphic import TableGraphic


class Visualizer:
    def __init__(self) -> None:
        self.text_graphic = TextGraphic()
        self.table_graphic = TableGraphic(4, 4)
        
    def visualize_text(self, *targets: List[List[Any]]):
        for target in targets:
            self.text_graphic.visualize(target)

    def visualize_table(self, *targets: List[List[float]]):
        for target in targets:
            self.table_graphic.visualize(target)
