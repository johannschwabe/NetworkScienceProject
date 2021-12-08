import numpy as np

from InterdependantNetwork import InterdependantNetwork
import networkx as nx


class ScaleFree(InterdependantNetwork):
    def __init__(self, nr_nodes):
        super().__init__(nr_nodes)

        self.graph_1 = nx.barabasi_albert_graph(nr_nodes, 2)
        self.graph_2 = nx.barabasi_albert_graph(nr_nodes, 2)

    def __str__(self):
        return f"Scale Free"

