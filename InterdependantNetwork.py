import random

import networkx as nx
import matplotlib.pyplot as plt


class InterdependantNetwork:
    def __init__(self, nr_nodes):
        self.graph_1 = None
        self.graph_2 = None
        self.graph_1_outgoing = {}
        self.graph_2_outgoing = {}
        self.nr_nodes = nr_nodes

    # generate "nr_connections" random interconnections between the two networks
    def interconnect_bidirectional(self):
        for connection in range(self.nr_nodes):
            self.graph_1_outgoing[connection] = connection
            self.graph_2_outgoing[connection] = connection

    def interconnect_unidirectional(self):
        self.connect_graphs(self.graph_1_outgoing)
        self.connect_graphs(self.graph_2_outgoing)

    def connect_graphs(self, outgoing):
        for connection in range(self.nr_nodes):
            rnd_node = random.randrange(self.nr_nodes)
            while rnd_node in outgoing.values():
                rnd_node = random.randrange(self.nr_nodes)
            outgoing[connection] = rnd_node

    def interconnected_graph(self):
        graph = nx.DiGraph()

        for node in self.graph_1:
            graph.add_node(f"1_{node}")
        for edge in self.graph_1.edges():
            graph.add_edge(f"1_{edge[0]}", f"1_{edge[1]}")
            graph.add_edge(f"1_{edge[1]}", f"1_{edge[0]}")

        for node in self.graph_2:
            graph.add_node(f"2_{node}")
        for edge in self.graph_2.edges():
            graph.add_edge(f"2_{edge[0]}", f"2_{edge[1]}")
            graph.add_edge(f"2_{edge[1]}", f"2_{edge[0]}")

        for key, val in self.graph_1_outgoing.items():
            graph.add_edge(f"1_{key}", f"2_{val}")

        for key, val in self.graph_2_outgoing.items():
            graph.add_edge(f"2_{key}", f"1_{val}")

        return graph

    def plot_graph(self, invalid_1, invalid_2):
        invalid_names_1 = [f"1_{node}" for node in invalid_1]
        invalid_names_2 = [f"2_{node}" for node in invalid_2]
        plt.figure()
        G = self.interconnected_graph()
        color_map = ["pink" if node in invalid_names_1 else "aquamarine" if node in invalid_names_2 else "red" if node[
                                                                                                                  :1] == "1" else "limegreen"
                     for node in G]
        nx.draw(G, node_color=color_map, with_labels=True)
        plt.show()

    # Remove a node from a given graph.
    # Returns a set of nodes that were interconnected with the removed node and are now invalid
    def destroy_node(self, node, network_nr):
        current_neti, other_neti, current_out, other_out = \
            (self.graph_1, self.graph_2, self.graph_1_outgoing, self.graph_2_outgoing) \
            if network_nr == 1 else \
            (self.graph_2, self.graph_1, self.graph_2_outgoing, self.graph_2_outgoing)

        if node in current_neti:
            current_neti.remove_node(node)

        # Remove interconnections
        for key, value in other_out.items():
            if node == value:
                other_out.pop(key)
                break
        if node in current_out:
            return current_out.pop(node)
        return None

    # Recursively removes nodes until a stable state is reached
    def cascade(self, kill_list_1, kill_list_2):
        invalid_1 = set([])  # Nodes to be removed in graph_1 in the next iteration
        invalid_2 = set([])  # Nodes to be removed in graph_2 in the next iteration

        # Remove previously marked nodes
        for random_node in kill_list_1:
            invalid = self.destroy_node(random_node, 1)
            if invalid is not None:
                invalid_2.add(invalid)
        for random_node in kill_list_2:
            invalid = self.destroy_node(random_node, 2)
            if invalid is not None:
                invalid_1.add(invalid)

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

        # plt.figure()
        # nx.draw(self.graph_1, with_labels=True)
        # plt.show()
        # plt.figure()
        # nx.draw(self.graph_2, with_labels=True)
        # plt.show()
        # self.plot_graph(invalid_1, invalid_2)

        # if no nodes are marked for removal, terminate. Else recurse
        if len(invalid_1.union(invalid_2)) > 0:
            self.cascade(invalid_1, invalid_2)

    # Destroy a given number of random nodes from each network
    def destroy_nodes(self, nodes_to_destroy):
        # plt.figure()
        # nx.draw(self.graph_1, with_labels=True)
        # plt.show()
        # plt.figure()
        # nx.draw(self.graph_2, with_labels=True)
        # plt.show()

        shuffled = list(range(self.nr_nodes))
        random.shuffle(shuffled)
        destroy = shuffled[:nodes_to_destroy]

        self.cascade(destroy, [])

    def clone(self):
        new_network = InterdependantNetwork(self.nr_nodes)
        new_network.graph_1 = nx.Graph(self.graph_1)
        new_network.graph_2 = nx.Graph(self.graph_2)
        new_network.graph_1_outgoing = self.graph_1_outgoing.copy()
        new_network.graph_2_outgoing = self.graph_2_outgoing.copy()
        return new_network

    def p_mu_n(self):
        connected_components = [len(c) for c in sorted(nx.connected_components(self.graph_1), key=len, reverse=True)]
        if len(connected_components) > 0:
            return connected_components[0] / self.nr_nodes
        return 0
