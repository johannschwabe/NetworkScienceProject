from InterdependentNetwork import InterdependentNetwork
import networkx as nx


class RandomRegular(InterdependentNetwork):
    def __init__(self, nr_nodes, deg, regular=False):
        super().__init__(nr_nodes)

        self.graph_1 = nx.random_regular_graph(deg, nr_nodes)

        if regular:
            return

        self.graph_2 = nx.random_regular_graph(deg, nr_nodes)

        # print("Graph1 con:", nx.is_connected(self.graph_1), "deg:", np.average([deg[1] for deg in self.graph_1.degree]))
        # print("Graph2 con:", nx.is_connected(self.graph_2), "deg:", np.average([deg[1] for deg in self.graph_2.degree]))

    def __str__(self):
        return "Random Regular"
