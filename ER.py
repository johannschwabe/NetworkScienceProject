import networkx as nx

from InterdependantNetwork import InterdependantNetwork


class ER(InterdependantNetwork):
    def __init__(self, nr_nodes, p):
        super().__init__(nr_nodes)
        self.graph_1 = nx.erdos_renyi_graph(nr_nodes, p)
        self.graph_2 = nx.erdos_renyi_graph(nr_nodes, p)

    def __str__(self):
        return "Erdos renyi"
