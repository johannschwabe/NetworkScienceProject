import matplotlib.pyplot as plt
import os
from ER import ER
from RandomRegular import RandomRegular
from ScaleFree import ScaleFree
import numpy as np
import networkx as nx
import random
import time
import pandas as pd


class Simulator:

    def __init__(self, nr_created_networks, nr_runs_per_network, range_start, range_end, range_nr_steps, bidir):
        # General parameters
        self.nr_created_networks = nr_created_networks  # defines how often the step of creating a network should be repeated
        self.nr_runs_per_network = nr_runs_per_network  # defines how often the killing should be repeated
        self.average_degree = 4
        self.remaining_nodes_options = np.linspace(range_start, range_end, range_nr_steps)  # start point (0 = 0%), end point (1 = 100%) and number
        self.bidir = bidir
        # of steps to generate plt 2


        # Networks analysis params
        self.nw_types = ["ER", "RR", "SF"]

        # Helpers: er analysis
        self.ns = []
        self.er_inter_names = []
        self.er_reg_names = []

        self.psk = []
        self.p_infinities_reg_er = []
        self.p_infinities_inter_er = []

        # Helpers: networks analysis
        self.names_part2 = []
        self.p_infinities_inter_part2 = []
        self.p_infinities_reg_part2 = []

    def create_network(self, nw_type, nr_nodes, inter=True):
        network = None
        if inter:
            if nw_type == "ER":
                network = ER(nr_nodes, self.average_degree / nr_nodes)
            elif nw_type == "RR":
                network = RandomRegular(nr_nodes, self.average_degree)
            elif nw_type == "SF":
                network = ScaleFree(nr_nodes)
            network.interconnect_bidirectional()
        else:
            if nw_type == "ER":
                network = nx.erdos_renyi_graph(nr_nodes, (self.average_degree / nr_nodes))
            elif nw_type == "RR":
                network = nx.random_regular_graph(self.average_degree, nr_nodes)
            elif nw_type == "SF":
                network = nx.barabasi_albert_graph(nr_nodes, 2)

        if network is not None and inter:
            if self.bidir:
                network.interconnect_bidirectional()
            else:
                network.interconnect_unidirectional()
        return network

    def simulate_killing(self, network, inter=True):
        p_infinities = []
        for p in self.remaining_nodes_options:
            gc_exists_list = []
            for m in range(self.nr_runs_per_network):
                if inter:
                    local_network = network.clone()
                    size = network.nr_nodes
                    nr_to_destroy = int(np.floor(local_network.nr_nodes * (1 - p)))
                    local_network.destroy_nodes(nr_to_destroy)
                    gc_exists_list.append(local_network.p_mu_n(size - nr_to_destroy))
                else:
                    local_network = nx.Graph(network)
                    nr_to_destroy = int(np.floor(len(local_network.nodes) * (1 - p)))
                    for i in range(nr_to_destroy):
                        local_network.remove_node(random.choice(list(local_network.nodes)))
                    # Calculate p infinity
                    connected_components = [len(c) for c in
                                            sorted(nx.connected_components(local_network), key=len, reverse=True)]
                    if len(connected_components) and connected_components[0] > 1:
                        p_mu = connected_components[0] / len(local_network.nodes)
                    else:
                        p_mu = 0
                    gc_exists_list.append(p_mu)
                # print("{} out of {} killing runs done".format(m, self.nr_of_runs_killing))
            print("{} calculated".format(p))
            p_infinities.append(np.mean(gc_exists_list))

        return p_infinities

    def plot_pk_infinity(self, p_infinities_nw, title):
        print(p_infinities_nw)
        plt.figure()
        for p_infinities in p_infinities_nw:
            plt.plot(self.psk, p_infinities)
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")
        plt.title(title)
        plt.legend(self.ns)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures', str(title) + ".png")
        plt.savefig(path)

    def plot_p_infinity(self, p_infinities_nw, title):
        plt.figure()
        for p_infinities in p_infinities_nw:
            plt.plot(self.remaining_nodes_options, p_infinities)
            plt.xlabel("p")
            plt.ylabel("P Infinity")
        plt.title(title)
        plt.legend(self.names_part2)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures', str(title) + ".png")
        plt.savefig(path)

    def analyse_inter_er_augmenting_n(self, er_start_n, er_nr_steps):
        # Ns from paper 1000, 2000, 4000 ... 64 000
        self.ns = []
        for i in range(0, er_nr_steps):
            self.ns.append(2 ** i * er_start_n)

        start_time = time.time()
        for n in self.ns:
            nw_time = time.time()
            print("Simulate network size {}. Time since start: {}".format(n, nw_time - start_time))
            n_p_infinities = []
            for i in range(self.nr_created_networks):
                print("Network {}: {} out of {} networks created".format(n, i, self.nr_created_networks))
                # 1. Create interdependent Erdos Renyi networks
                er_network = ER(n, self.average_degree / n)
                if self.bidir:
                    er_network.interconnect_bidirectional()
                else:
                    er_network.interconnect_unidirectional()
                # 2. Perform cascading failure M times for increasing p to calculate pInfinity
                p_infinities = self.simulate_killing(er_network)
                n_p_infinities.append(p_infinities)
            self.p_infinities_inter_er.append(np.array(n_p_infinities).mean(axis=0))
            self.er_inter_names.append("Interdependent ER Network " + str(self.average_degree) + " " + str(n))
        # self.p_infinities_inter_er = np.array(self.p_infinities_inter_er).mean(axis=0)

        # 2.2 make ps to psk
        self.psk = [element * self.average_degree for element in self.remaining_nodes_options]

        # 3. Draw scatter plot
        self.plot_pk_infinity(list(self.p_infinities_inter_er), f"Comparison interdependent ER with different N er_start_n: {er_start_n}, er_nr_steps {er_nr_steps}")

    def analyse_reg_er_augmenting_n(self, er_start_n, er_nr_steps):

        # Ns from paper 1000, 2000, 4000 ... 64 000
        self.ns = []
        for i in range(er_nr_steps):
            self.ns.append(2 ** i * er_start_n)

        start_time = time.time()
        for n in self.ns:
            nw_time = time.time()
            print("Simulate network size {}. Time since start: {}".format(n, nw_time - start_time))
            n_p_infinities = []
            for i in range(self.nr_created_networks):
                print("Network {}: {} out of {} networks created".format(n, i, self.nr_created_networks))
                # 1. Create regular Erdos Renyi networks
                er_network = nx.erdos_renyi_graph(n, self.average_degree / n)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(er_network, inter=False)
                n_p_infinities.append(p_infinities)
            self.p_infinities_reg_er.append(np.array(n_p_infinities).mean(axis=0))
            self.er_reg_names.append("Regular ER Network " + str(self.average_degree) + " " + str(n))

        # 2.2 make ps to psk
        self.psk = [element * self.average_degree for element in self.remaining_nodes_options]

        # 4. Draw scatter plot
        self.plot_pk_infinity(self.p_infinities_reg_er, f"Comparison regular ER with different N er_start_n: {er_start_n}, er_nr_steps {er_nr_steps}")

    def compare_inter_reg_er(self):
        for p_inf_inter_er, p_inf_reg_er, name, n in zip(self.p_infinities_inter_er, self.p_infinities_reg_er,
                                                         self.er_inter_names, self.ns):
            plt.figure()
            plt.plot(self.psk, p_inf_inter_er, color='red')
            plt.plot(self.psk, p_inf_reg_er, color='blue')
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular ER network for N = " + str(n))
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', str(name) + ".png")
            plt.savefig(path)

    def analyse_inter_networks_augmenting_n(self, nr_nodes):

        # 1. Create Networks
        self.names_part2.append("ER")
        self.names_part2.append("RR")
        self.names_part2.append("SF")

        start_time = time.time()
        for nw_type in self.nw_types:
            nw_time = time.time()
            print("Simulate network type {}. Time elapsed since start: {}".format(nw_type, nw_time - start_time))
            n_p_infinities = []
            for i in range(self.nr_created_networks):
                print("Network {}: {} out of {} networks created".format(nw_type, i, self.nr_created_networks))
                # 1. Create network
                network = self.create_network(nw_type, nr_nodes)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(network)
                n_p_infinities.append(p_infinities)
            self.p_infinities_inter_part2.append(np.array(n_p_infinities).mean(axis=0))
        # 3. plot
        self.plot_p_infinity(self.p_infinities_inter_part2, f"Comparison Interdependent Networks nr_nodes: {nr_nodes}")

    def analyse_reg_networks_augmenting_n(self, nr_nodes):
        # 1. Create Networks
        self.names_part2.append("ER")
        self.names_part2.append("RR")
        self.names_part2.append("SF")

        start_time = time.time()
        for nw_type in self.nw_types:
            nw_time = time.time()
            print("Simulate network type {}. Time elapsed since start: {}".format(nw_type, nw_time - start_time))
            n_p_infinities = []
            for i in range(self.nr_created_networks):
                print("Network {}: {} out of {} networks created".format(nw_type, i, self.nr_created_networks))
                # 1. Create network
                network = self.create_network(nw_type, nr_nodes, False)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(network, inter=False)
                n_p_infinities.append(p_infinities)
            self.p_infinities_reg_part2.append(np.array(n_p_infinities).mean(axis=0))
        # 3. plot
        self.plot_p_infinity(self.p_infinities_reg_part2, f"Comparison Regular Networks nr_nodes: {nr_nodes}")

    def compare_inter_reg_part2(self):
        for p_inf_inter, p_inf_reg, name in zip(self.p_infinities_inter_part2, self.p_infinities_reg_part2,
                                                self.names_part2):
            plt.figure()
            plt.plot(self.remaining_nodes_options, p_inf_inter, color='red')
            plt.plot(self.remaining_nodes_options, p_inf_reg, color='blue')
            plt.xlabel("p")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular {} Network".format(name))
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', str(name) + ".png")
            plt.savefig(path)

    def save_results(self):
        directory = os.path.dirname(__file__)

        if len(self.p_infinities_inter_er) > 0:
            path = os.path.join(directory, 'results', "results_inter_er.csv")
            p_infinities = np.array(self.p_infinities_inter_er).transpose()
            results = pd.DataFrame(p_infinities, columns=self.ns)
            results['psk'] = self.psk
            results.to_csv(path)

        if len(self.p_infinities_reg_er) > 0:
            path = os.path.join(directory, 'results', "results_reg_er.csv")
            p_infinities = np.array(self.p_infinities_reg_er).transpose()
            results = pd.DataFrame(p_infinities, columns=self.ns)
            results['psk'] = self.psk
            results.to_csv(path)

        if len(self.p_infinities_inter_part2) > 0:
            path = os.path.join(directory, 'results', "results_inter_networks.csv")
            p_infinities = np.array(self.p_infinities_inter_part2).transpose()
            results = pd.DataFrame(p_infinities, columns=self.nw_types)
            results['psk'] = self.remaining_nodes_options
            results.to_csv(path)

        if len(self.p_infinities_reg_part2) > 0:
            path = os.path.join(directory, 'results', "results_reg_networks.csv")
            p_infinities = np.array(self.p_infinities_reg_part2).transpose()
            results = pd.DataFrame(p_infinities, columns=self.nw_types)
            results['psk'] = self.remaining_nodes_options
            results.to_csv(path)
