import numpy as np

from InterdependantNetwork import InterdependantNetwork
import networkx as nx


class ScaleFree(InterdependantNetwork):
    def __init__(self, nr_nodes, expo, avg):
        super().__init__(nr_nodes)
        sequence = np.array(nx.utils.powerlaw_sequence(nr_nodes, expo))
        avg_deg = np.average(sequence)
        # avg_deg = avg
        new_seq = np.array(np.round(sequence * avg/avg_deg), dtype=int)
        if np.sum(new_seq) % 2 == 1:
            new_seq[0] += 1

        self.graph_1 = nx.configuration_model(new_seq)
        self.graph_2 = nx.configuration_model(new_seq)
        self.avg = avg
        self.expo = expo

    def __str__(self):
        return f"Scale Free: {self.expo}"

