import numpy as np

from InterdependantNetwork import InterdependantNetwork
import networkx as nx


class ScaleFree(InterdependantNetwork):
    def __init__(self, nr_nodes, expo):
        super().__init__(nr_nodes)
        sequence = np.array(nx.utils.powerlaw_sequence(nr_nodes, expo), dtype=int)
        if np.sum(sequence) % 2 == 1:
            sequence[0] += 1

        self.graph_1 = nx.configuration_model(sequence)
        self.graph_2 = nx.configuration_model(sequence)
        self.expo = expo

    def __str__(self):
        return f"Scale Free: {self.expo}"

