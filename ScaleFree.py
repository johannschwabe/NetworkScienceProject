import matplotlib.pyplot as plt
import numpy as np

from InterdependentNetwork import InterdependentNetwork
import networkx as nx
import networkx.utils.random_sequence as rs


class ScaleFree(InterdependentNetwork):
    Hurwitz_zeta_precomp = {}

    def __init__(self, nr_nodes, _lambda, regular=False):
        super().__init__(nr_nodes)
        sequence_1 = self.distribution(_lambda, nr_nodes)

        if sum(sequence_1) % 2 == 1:
            sequence_1[0] += 1

        self.graph_1 = nx.configuration_model(sequence_1)
        if regular:
            return
        sequence_2 = self.distribution(_lambda, nr_nodes)

        if sum(sequence_2) % 2 == 1:
            sequence_2[0] += 1
        self.graph_2 = nx.configuration_model(sequence_2)
        # self.graph_1 = nx.barabasi_albert_graph(nr_nodes, 2)
        # self.graph_2 = nx.barabasi_albert_graph(nr_nodes, 2)

    def __str__(self):
        return f"Scale Free"

    def Hurwitz_zeta(self, alpha, x_min):
        if x_min in ScaleFree.Hurwitz_zeta_precomp:
            return ScaleFree.Hurwitz_zeta_precomp[x_min]
        inter = 0
        aggri = 0
        change = 1
        while change > 0.00001:
            change = np.power(float(inter + x_min), -alpha)
            aggri += change
            inter += 1
        ScaleFree.Hurwitz_zeta_precomp[x_min] = aggri
        return aggri

    def power_law(self, x, alpha, x_min):
        return np.power(float(x), -alpha) / self.Hurwitz_zeta(alpha, x_min)

    def distribution(self, alpha, n):
        _range = 20000
        # x_min = int(4 * (alpha-2)/(alpha-1))
        x_min = 3
        hist = [self.power_law(_iter, alpha, x_min) for _iter in range(1, _range)]
        hist = [0] * int(x_min) + hist
        return rs.discrete_sequence(n, hist)
