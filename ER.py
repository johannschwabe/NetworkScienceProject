import networkx as nx

from InterdependentNetwork import InterdependentNetwork


class ER(InterdependentNetwork):
    def __init__(self, nr_nodes, p, regular=False):
        super().__init__(nr_nodes)

        self.graph_1 = nx.random_reference(nx.erdos_renyi_graph(nr_nodes, p))

        if regular:
            return

        self.graph_2 = nx.random_reference(nx.erdos_renyi_graph(nr_nodes, p))

    def __str__(self):
        return "Erdos renyi"
