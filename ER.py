import random

import networkx as nx

from InterdependentNetwork import InterdependentNetwork


class ER(InterdependentNetwork):
    def __init__(self, nr_nodes, p, regular=False):
        super().__init__(nr_nodes)

        self.graph_1 = nx.erdos_renyi_graph(nr_nodes, p)
        comps = list(nx.connected_components(self.graph_1))

        while len(comps) > 1:
            random.shuffle(comps)
            self.graph_1.add_edge(random.choice(list(comps[0])), random.choice(list(comps[1])))
            comps = list(nx.connected_components(self.graph_1))

        if regular:
            return

        self.graph_2 = nx.erdos_renyi_graph(nr_nodes, p)
        comps = list(nx.connected_components(self.graph_2))

        while len(comps) > 1:
            random.shuffle(comps)
            self.graph_2.add_edge(random.choice(list(comps[0])), random.choice(list(comps[1])))
            comps = list(nx.connected_components(self.graph_2))

        # print("Graph1 con:", nx.is_connected(self.graph_1), "deg:", np.average([deg[1] for deg in self.graph_1.degree]))
        # print("Graph2 con:", nx.is_connected(self.graph_2), "deg:", np.average([deg[1] for deg in self.graph_2.degree]))

    def __str__(self):
        return "Erdos renyi"
