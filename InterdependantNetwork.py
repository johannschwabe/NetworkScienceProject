import random

import networkx as nx
import matplotlib.pyplot as plt

class InterdependantNetwork:
    def __init__(self, nr_nodes_1, nr_nodes_2):
        self.graph_1 = None
        self.graph_2 = None
        self.nr_nodes_1 = nr_nodes_1
        self.nr_nodes_2 = nr_nodes_2
        self.interconnection = {}       # Dictionary with keys: {network_nr}_{node_nr} and values node_nr[]

    # generate "nr_connections" random interconnections between the two networks
    def interconnect(self, nr_connections):
        interconnections = [(random.randrange(0, self.nr_nodes_1), random.randrange(0, self.nr_nodes_2)) for _ in
             range(nr_connections)]
        for connection in interconnections:

            # Generated connections are bi-directional but are saved as uni-directional: each connection is added twice
            key = f"1_{connection[0]}"
            if key in self.interconnection:
                self.interconnection[key].append(connection[1])
            else:
                self.interconnection[key] = [connection[1]]

            key = f"2_{connection[1]}"
            if key in self.interconnection:
                self.interconnection[key].append(connection[0])
            else:
                self.interconnection[key] = [connection[0]]

    # Remove a node from a given graph.
    # Returns a set of nodes that were interconnected with the removed node and are now invalid
    def destroy_node(self, node, network_nr):
        current_neti, other_neti = (self.graph_1, self.graph_2) if network_nr == 1 else (self.graph_2, self.graph_1)
        current_neti.remove_node(node)
        for key, value in self.interconnection.items():
            if node in value and key[:1] != f"{network_nr}":
                while node in value:
                    value.remove(node)
        key = f"{network_nr}_{node}"
        if key in self.interconnection:
            return set(self.interconnection.pop(key))
        return set([])

    # Recursively removes nodes until a stable state is reached
    def cascade(self, kill_list_1, kill_list_2):
        invalid_1 = set([])     # Nodes to be removed in graph_1 in the next iteration
        invalid_2 = set([])     # Nodes to be removed in graph_2 in the next iteration

        # print("---------------------")
        # print("Deleting in N1:")
        # print(kill_list_1)
        # print("Current:")
        # print(self.graph_1.nodes)
        # print("Deleting in N2:")
        # print(kill_list_2)
        # print("Current:")
        # print(self.graph_2.nodes)

        # Remove previously marked nodes
        for random_node in kill_list_1:
            invalid_2 = invalid_2.union(self.destroy_node(random_node, 1))
        for random_node in kill_list_2:
            invalid_1 = invalid_1.union(self.destroy_node(random_node, 2))

        # Make shure that nodes removed this round aren't falsy removed again next round
        invalid_1 = invalid_1.difference(kill_list_1)
        invalid_2 = invalid_2.difference(kill_list_2)

        # Remove nodes not belonging to the giant component
        g_1_not_giants = sorted(nx.connected_components(self.graph_1), key=len)[:-1]
        for not_giant in g_1_not_giants:
            invalid_1 = invalid_1.union(not_giant)

        g_2_not_giants = sorted(nx.connected_components(self.graph_2), key=len)[:-1]
        for not_giant in g_2_not_giants:
            invalid_2 = invalid_2.union(not_giant)

        # if no nodes are marked for removal, terminate. Else recurse
        if len(invalid_1.union(invalid_2)) > 0:
            self.cascade(invalid_1, invalid_2)

    # Destroy a given number of random nodes from each network
    def destroy_nodes(self, nodes_to_destroy_1, nodes_to_destroy_2):
        plt.figure()
        nx.draw(self.graph_1, with_labels=True)
        plt.show()
        plt.figure()
        nx.draw(self.graph_2, with_labels=True)
        plt.show()

        shuffled_1 = list(range(self.nr_nodes_1))
        shuffled_2 = list(range(self.nr_nodes_2))
        random.shuffle(shuffled_1)
        random.shuffle(shuffled_2)

        self.cascade(shuffled_1[:nodes_to_destroy_1], shuffled_2[:nodes_to_destroy_2])
        plt.figure()
        nx.draw(self.graph_1, with_labels=True)
        plt.show()
        plt.figure()
        nx.draw(self.graph_2, with_labels=True)
        plt.show()

