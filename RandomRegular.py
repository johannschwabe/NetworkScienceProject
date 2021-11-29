from InterdependantNetwork import InterdependantNetwork
import networkx as nx


class RandomRegular(InterdependantNetwork):
    def __init__(self, nr_nodes_1, nr_nodes_2, deg_1, deg_2):
        super().__init__(nr_nodes_1, nr_nodes_2)
        self.graph_1 = nx.random_regular_graph(deg_1, nr_nodes_1)
        self.graph_2 = nx.random_regular_graph(deg_2, nr_nodes_2)
