import numpy as np

from InterdependantNetwork import InterdependantNetwork
import networkx as nx


class ScaleFree(InterdependantNetwork):
    def __init__(self, nr_nodes_1, nr_nodes_2, expo_1, expo_2, avg_1, avg_2):
        super().__init__(nr_nodes_1, nr_nodes_2)
        sequence1 = nx.utils.powerlaw_sequence(nr_nodes_1, expo_1)
        avg = np.average(sequence1)
        new_seq_1 = np.array(np.round(sequence1 * avg_1/avg), dtype=int)
        if np.sum(new_seq_1) % 2 == 1:
            new_seq_1[0] += 1

        sequence2 = nx.utils.powerlaw_sequence(nr_nodes_2, expo_2)
        avg = np.average(sequence2)
        new_seq_2 = np.array(np.round(sequence2 * avg_2 / avg), dtype=int)
        if np.sum(new_seq_2) % 2 == 1:
            new_seq_2[0] += 1

        self.graph_1 = nx.configuration_model(new_seq_1)
        self.graph_2 = nx.configuration_model(new_seq_2)

    def __str__(self):
        return "Scale Free"

