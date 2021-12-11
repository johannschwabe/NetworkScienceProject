from InterdependentNetwork import InterdependentNetwork
import networkx as nx


class RandomRegular(InterdependentNetwork):
    def __init__(self, nr_nodes, deg):
        super().__init__(nr_nodes)
        self.graph_1 = nx.random_regular_graph(deg, nr_nodes)
        self.graph_2 = nx.random_regular_graph(deg, nr_nodes)

    def __str__(self):
        return "Random Regular"
