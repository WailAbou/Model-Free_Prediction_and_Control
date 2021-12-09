from typing import Any, List


class Visualizer:
    def print_grids(self, *targets: List[List[Any]]) -> None:
        for target in targets:
            rows, cols = len(target), len(target[0])
            print('\n\n ', ''.join([f" | {' ':10s}{str(i):10s} |" for i in range(rows)]))
            for row in range(len(target)):
                print('  ' + '-' * cols * 25)
                print(row, ''.join([f" | {str(target[row][col]):20s} |" for col in range(cols)]))
                print('  ' + '_' * cols * 25)
