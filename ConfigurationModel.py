from InterdependentNetwork import InterdependentNetwork
import networkx as nx


class ConfigurationModel(InterdependentNetwork):
    def __init__(self, nr_nodes, gamma):
        super().__init__(nr_nodes)
        sequence = nx.random_powerlaw_tree_sequence(nr_nodes, gamma=gamma, tries=5000)
        self.graph_1 = nx.configuration_model(sequence)
        self.graph_2 = nx.configuration_model(sequence)

    def __str__(self):
        return "Configuration Model"
