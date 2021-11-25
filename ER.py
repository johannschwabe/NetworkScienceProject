import networkx as nx

from InterdependantNetwork import InterdependantNetwork


class ER(InterdependantNetwork):
    def __init__(self, nr_nodes_1, nr_nodes_2, nr_edges_1, nr_edges_2):
        super().__init__(nr_nodes_1, nr_nodes_2)
        self.graph_1 = nx.gnm_random_graph(nr_nodes_1, nr_edges_1)
        self.graph_2 = nx.gnm_random_graph(nr_nodes_2, nr_edges_2)
