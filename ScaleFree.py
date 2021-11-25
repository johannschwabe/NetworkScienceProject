from InterdependantNetwork import InterdependantNetwork
import networkx as nx


class ScaleFree(InterdependantNetwork):
    def __init__(self, nr_nodes_1, nr_nodes_2, alpha_1, alpha_2, beta_1, beta_2):
        super().__init__(nr_nodes_1, nr_nodes_2)
        self.graph_1 = nx.Graph(nx.to_undirected(nx.scale_free_graph(nr_nodes_1, alpha=alpha_1, beta=beta_1)))
        self.graph_2 = nx.Graph(nx.to_undirected(nx.scale_free_graph(nr_nodes_2, alpha=alpha_2, beta=beta_2)))
