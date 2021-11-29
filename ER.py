import networkx as nx

from InterdependantNetwork import InterdependantNetwork


class ER(InterdependantNetwork):
    def __init__(self, nr_nodes_1, nr_nodes_2, p_1, p_2):
        super().__init__(nr_nodes_1, nr_nodes_2)
        self.graph_1 = nx.erdos_renyi_graph(nr_nodes_1, p_1)
        self.graph_2 = nx.erdos_renyi_graph(nr_nodes_2, p_2)

    def __str__(self):
        return "Erdos renyi"
