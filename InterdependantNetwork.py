import random

import networkx as nx
import matplotlib.pyplot as plt


class InterdependantNetwork:
    def __init__(self, nr_nodes_1, nr_nodes_2):
        self.graph_1 = None
        self.graph_2 = None
        self.nr_nodes_1 = nr_nodes_1
        self.nr_nodes_2 = nr_nodes_2
        self.interconnection = {}  # Dictionary with keys: {network_nr}_{node_nr} and values node_nr[]

    # generate "nr_connections" random interconnections between the two networks
    def interconnect_bidirectional(self, nr_connections):
        self.interconnection = {}  # Dictionary with keys: {network_nr}_{node_nr} and values node_nr[]

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

    def interconnect_unidirectional(self, nr_connections_1, nr_connections_2):
        self.interconnection = {}  # Dictionary with keys: {network_nr}_{node_nr} and values node_nr[]

        interconnections_1 = [(random.randrange(0, self.nr_nodes_1), random.randrange(0, self.nr_nodes_2)) for _ in
                              range(nr_connections_1)]
        interconnections_2 = [(random.randrange(0, self.nr_nodes_2), random.randrange(0, self.nr_nodes_1)) for _ in
                              range(nr_connections_2)]

        for connection_1 in interconnections_1:
            # Generated connections are uni-directional
            key = f"1_{connection_1[0]}"
            if key in self.interconnection:
                self.interconnection[key].append(connection_1[1])
            else:
                self.interconnection[key] = [connection_1[1]]

        for connection_2 in interconnections_2:
            # Generated connections are uni-directional
            key = f"2_{connection_2[0]}"
            if key in self.interconnection:
                self.interconnection[key].append(connection_2[1])
            else:
                self.interconnection[key] = [connection_2[1]]

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

        for key, val in self.interconnection.items():
            for target in val:
                if key[:1] == "1":
                    graph.add_edge(key, f"2_{target}")
                else:
                    graph.add_edge(key, f"1_{target}")

        return graph

    def plot_graph(self, invalid_1, invalid_2):
        invalid_names_1 = [f"1_{node}" for node in invalid_1]
        invalid_names_2 = [f"2_{node}" for node in invalid_2]
        plt.figure()
        G = self.interconnected_graph()
        color_map = ["pink" if node in invalid_names_1 else "aquamarine" if node in invalid_names_2 else "red" if node[:1] == "1" else "limegreen" for node in G]
        nx.draw(G, node_color=color_map, with_labels=True)
        plt.show()

    # Remove a node from a given graph.
    # Returns a set of nodes that were interconnected with the removed node and are now invalid
    def destroy_node(self, node, network_nr):
        current_neti, other_neti = (self.graph_1, self.graph_2) if network_nr == 1 else (self.graph_2, self.graph_1)
        # Remove all edges
        current_neti.remove_node(node)
        # current_neti.add_node(node)
        # Remove interconnections
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
        invalid_1 = set([])  # Nodes to be removed in graph_1 in the next iteration
        invalid_2 = set([])  # Nodes to be removed in graph_2 in the next iteration

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

        # plt.figure()
        # nx.draw(self.graph_1, with_labels=True)
        # plt.show()
        # plt.figure()
        # nx.draw(self.graph_2, with_labels=True)
        # plt.show()
        self.plot_graph(invalid_1, invalid_2)

        # if no nodes are marked for removal, terminate. Else recurse
        if len(invalid_1.union(invalid_2)) > 0:
            self.cascade(invalid_1, invalid_2)

    # Destroy a given number of random nodes from each network
    def destroy_nodes(self, nodes_to_destroy_1, nodes_to_destroy_2):
        # plt.figure()
        # nx.draw(self.graph_1, with_labels=True)
        # plt.show()
        # plt.figure()
        # nx.draw(self.graph_2, with_labels=True)
        # plt.show()


        shuffled_1 = list(range(self.nr_nodes_1))
        shuffled_2 = list(range(self.nr_nodes_2))
        random.shuffle(shuffled_1)
        random.shuffle(shuffled_2)

        destroy_1 = shuffled_1[:nodes_to_destroy_1]
        destroy_2 = shuffled_2[:nodes_to_destroy_2]

        self.plot_graph(destroy_1, destroy_2)

        self.cascade(destroy_1, destroy_2)
