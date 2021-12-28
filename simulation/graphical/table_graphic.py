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
        cstart = (self.w + 1) * (self.w + 1)
        trianglesN = [(i + j * (self.w + 1), i + 1 + j * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        trianglesE = [(i + 1 + j * (self.w + 1), i + 1 + (j + 1) * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        trianglesS = [(i + 1 + (j + 1) * (self.w + 1), i + (j + 1) * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        trianglesW = [(i + (j + 1) * (self.w + 1), i + j * (self.w + 1), cstart + i + j * self.w) for j in range(self.h) for i in range(self.w)]
        return [Triangulation(x, y, triangles) for triangles in [trianglesN, trianglesE, trianglesS, trianglesW]]
    
    def visualize(self, values):
        fig, ax = plt.subplots()
        triangul = self.triangulation_for_triheatmap()
        imgs = [ax.tripcolor(t, np.ravel(val), cmap='RdYlGn', vmin=0, vmax=1, ec='white') for t, val in zip(triangul, values)]

        for val, dir in zip(values, [(-1, 0), (0, 1), (1, 0), (0, -1)]):
            for i in range(self.w):
                for j in range(self.h):
                    v = val[i][j]
                    ax.text(i + 0.3 * dir[1], j + 0.3 * dir[0], f'{v:.3f}', color='k' if 0.2 < v < 0.8 else 'w', ha='center', va='center')
        
        fig.colorbar(imgs[0], ax=ax)
        ax.set_xticks(range(self.w))
        ax.set_yticks(range(self.h))
        ax.invert_yaxis()
        ax.margins(x=0, y=0)
        ax.set_aspect('equal', 'box')

        plt.tight_layout()
        plt.show()
