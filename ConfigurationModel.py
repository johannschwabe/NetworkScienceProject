from InterdependantNetwork import InterdependantNetwork
import networkx as nx

class ConfigurationModel(InterdependantNetwork):
    def __init__(self, nr_nodes_1, nr_nodes_2, gamma_1, gamma_2):
        super().__init__(nr_nodes_1, nr_nodes_2)
        sequence_1 = nx.random_powerlaw_tree_sequence(nr_nodes_1, gamma=gamma_1, tries=5000)
        sequence_2 = nx.random_powerlaw_tree_sequence(nr_nodes_2, gamma=gamma_2, tries=5000)
        self.graph_1 = nx.configuration_model(sequence_1)
        self.graph_2 = nx.configuration_model(sequence_2)
