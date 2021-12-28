from matplotlib import pyplot as plt
from matplotlib.tri import Triangulation
import numpy as np


class TableGraphic:
    def __init__(self, w, h) -> None:
        self.w = w
        self.h = h

    def triangulation_for_triheatmap(self):
        xv, yv = np.meshgrid(np.arange(-0.5, self.w), np.arange(-0.5, self.h))
        xc, yc = np.meshgrid(np.arange(0, self.w), np.arange(0, self.h))
        x = np.concatenate([xv.ravel(), xc.ravel()])
        y = np.concatenate([yv.ravel(), yc.ravel()])
        cstart = (self.w + 1) * (self.h + 1)
        trianglesN = [(i + j * (self.w + 1), i + 1 + j * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        trianglesE = [(i + 1 + j * (self.w + 1), i + 1 + (j + 1) * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        trianglesS = [(i + 1 + (j + 1) * (self.w + 1), i + (j + 1) * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        trianglesW = [(i + (j + 1) * (self.w + 1), i + j * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        return [Triangulation(x, y, triangles) for triangles in [trianglesN, trianglesE, trianglesS, trianglesW]]
    
    def visualize(self, values):
        figure, axis = plt.subplots()
        trianguls = self.triangulation_for_triheatmap()
        imgs = [axis.tripcolor(triangul, np.ravel(value, order='F'), cmap='RdYlGn', vmin=0, vmax=1, ec='white') for triangul, value in zip(trianguls, values)]

        for val, dir in zip(values, [(0, -1), (1, 0), (0, 1), (-1, 0)]):
            for i in range(self.w):
                for j in range(self.h):
                    value = val[i][j]
                    color = 'k' if 0.2 < value < 0.8 else 'w'
                    axis.text(i + 0.3 * dir[0], j + 0.3 * dir[1], f'{value:.3f}', color=color, ha='center', va='center')
        
        figure.colorbar(imgs[0], ax=axis)
        axis.set_xticks(range(self.w))
        axis.set_yticks(range(self.h))
        axis.invert_yaxis()
        axis.margins(x=0, y=0)
        axis.set_aspect('equal', 'box')

        plt.tight_layout()
        plt.show()
