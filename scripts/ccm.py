import numpy as np
from scipy.stats.stats import pearsonr
import skccm.data as data
import matplotlib.pyplot as plt


class CCM(object):

    def __init__(self, data1, data2, dimension_E=2, delta_T=1):
        self.data1 = data1
        self.data2 = data2
        self.dimension_E = dimension_E
        self.delta_T = delta_T
        self.first = delta_T * (dimension_E - 1) + 1
        self.last = len(data1)
        self.manifold = []
        self.neighbors = []
        self.weights = []
        self.estimate_y = []
        self.e = np.e
        self.result = 0

    def shadow_manifold(self):
        for i in range(self.first - 1, self.last):
            self.manifold.append(
                self.data1[i - (self.dimension_E - 1) * self.delta_T:
                           i + 1:
                           self.delta_T])

    def nearest_neighbors(self):
        delta = 0.000000001
        manifold_len = len(self.manifold)
        self.distances = [[float('inf')] * manifold_len
                          for _ in range(manifold_len)]
        for i in range(manifold_len - 1):
            for j in range(i, manifold_len):
                d1, d2 = self.manifold[i], self.manifold[j]
                dist = [(x1 - x2)**2 + delta for x1, x2 in zip(d1, d2)]
                dist = sum(dist) ** 0.5
                self.distances[i][j] = dist
                self.distances[j][i] = dist

    def weight_estimate_y(self):
        for dists in self.distances:
            indices = sorted(range(len(dists)), key=lambda k: dists[k])
            indices = indices[:self.dimension_E + 1]
            self.neighbors.append(indices)
            # calculate weight
            ordered_dists = [dists[i] for i in indices]
            d1 = ordered_dists[0]
            uis = [self.e**(-di / d1) for di in ordered_dists]
            N = float(sum(uis))
            weights = [ui / N for ui in uis]
            self.weights.append(weights)
            pred_y = 0
            for i, w in zip(indices, weights):
                pred_y += self.data2[i] * w
            self.estimate_y.append(pred_y)

    def compute_correlation(self):
        p, _ = pearsonr(np.array(self.data2[self.first - 1: self.last]),
                        np.array(self.estimate_y))
        self.result = p ** 2

    def run(self):
        self.shadow_manifold()
        self.nearest_neighbors()
        self.weight_estimate_y()
        self.compute_correlation()


def test_data():
    rx1 = 3.72  # determines chaotic behavior of the x1 series
    rx2 = 3.72  # determines chaotic behavior of the x2 series
    b12 = 0.2  # Influence of x1 on x2
    b21 = 0.01  # Influence of x2 on x1
    ts_length = 1000
    x1, x2 = data.coupled_logistic(rx1, rx2, b12, b21, ts_length)
    libs = range(10, 1000, 50)
    res1, res2 = [], []
    for lib in libs:
        ccm1 = CCM(x1[:lib], x2[:lib], 2, 1)
        ccm1.run()
        res1.append(ccm1.result)
        ccm2 = CCM(x2[:lib], x1[:lib], 2, 1)
        ccm2.run()
        res2.append(ccm2.result)
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(libs, res1, c='r', ls='-')
    ax.plot(libs, res2, c='g', ls='-')
    plt.draw()
    plt.show()


if __name__ == '__main__':
    test_data()
