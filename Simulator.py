import os
import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from ER import ER
from RandomRegular import RandomRegular
from ScaleFree import ScaleFree


class Simulator:

    def __init__(self, nr_created_networks, nr_runs_per_network, range_start, range_end, range_nr_steps):
        # General parameters
        # defines how often the step of creating a network should be repeated
        self.nr_created_networks = nr_created_networks
        # defines how often the killing should be repeated
        self.nr_runs_per_network = nr_runs_per_network
        self.average_degree = 4
        # start point (0 = 0%), end point (1 = 100%) and number of steps
        self.remaining_nodes_options = np.linspace(range_start, range_end, range_nr_steps)
        # of steps to generate plt 2

        # Networks analysis params
        self.nw_types = ["ER", "RR", "SF_2.3", "SF_2.7", "SF_3.0"]

        # Helpers: er analysis
        self.ns = []

        self.psk_unidir = []
        self.psk_bidir = []
        self.psk_reg = []
        self.p_infinities_reg_er = []
        self.p_infinities_inter_unidir_er = []
        self.p_infinities_inter_bidir_er = []

        # Helpers: networks analysis
        self.names_part2 = []
        self.p_infinities_reg_ns = []
        self.p_infinities_inter_unidir_ns = []
        self.p_infinities_inter_bidir_ns = []

    def create_network(self, nw_type, nr_nodes, bidir, inter=True):
        network = None
        if inter:
            print(nw_type)
            if nw_type == "ER":
                network = ER(nr_nodes, self.average_degree / nr_nodes)
            elif nw_type == "RR":
                network = RandomRegular(nr_nodes, self.average_degree)
            elif nw_type == "SF_2.3":
                network = ScaleFree(nr_nodes, 2.3)
            elif nw_type == "SF_2.7":
                network = ScaleFree(nr_nodes, 2.7)
            elif nw_type == "SF_3.0":
                network = ScaleFree(nr_nodes, 3.0)
            network.interconnect_bidirectional()
        else:
            if nw_type == "ER":
                network = nx.erdos_renyi_graph(nr_nodes, (self.average_degree / nr_nodes))
            elif nw_type == "RR":
                network = nx.random_regular_graph(self.average_degree, nr_nodes)
            elif nw_type == "SF_2.3":
                network = ScaleFree(nr_nodes, 2.3, True).graph_1
            elif nw_type == "SF_2.7":
                network = ScaleFree(nr_nodes, 2.7, True).graph_1
            elif nw_type == "SF_3.0":
                network = ScaleFree(nr_nodes, 3.0, True).graph_1

        if network is not None and inter:
            if bidir:
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

    def plot_pk_infinity(self, p_infinities_nw, title, bidir, reg, nw_type_for_path="network"):
        plt.rcParams["figure.figsize"] = (6, 4)
        plt.figure()
        for p_infinities in p_infinities_nw:
            if reg:
                plt.plot(self.psk_reg, p_infinities)
            elif bidir:
                plt.plot(self.psk_bidir, p_infinities)
            else:
                plt.plot(self.psk_unidir, p_infinities)
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")

        plt.title(title, fontsize=9)
        plt.legend(self.ns)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures',
                            nw_type_for_path + ("Bidir" if bidir else "Unidir") + str(int(time.time())) + ".png")
        plt.savefig(path)

    def plot_p_infinity(self, p_infinities_nw, title, bidir, nw_type_for_path="network"):
        plt.rcParams["figure.figsize"] = (6, 4)
        plt.figure()
        for p_infinities in p_infinities_nw:
            plt.plot(self.remaining_nodes_options, p_infinities)
            plt.xlabel("p")
            plt.ylabel("P Infinity")

        plt.title(title, fontsize=9)
        plt.legend(self.names_part2)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures',
                            nw_type_for_path + ("Bidir" if bidir else "Unidir") + str(int(time.time())) + ".png")
        plt.savefig(path)

    def analyse_inter_er_augmenting_n(self, er_start_n, er_nr_steps, bidir):
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
                if bidir:
                    er_network.interconnect_bidirectional()
                else:
                    er_network.interconnect_unidirectional()
                # 2. Perform cascading failure M times for increasing p to calculate pInfinity
                p_infinities = self.simulate_killing(er_network)
                n_p_infinities.append(p_infinities)

            if bidir:
                self.p_infinities_inter_bidir_er.append(np.array(n_p_infinities).mean(axis=0))
            else:
                self.p_infinities_inter_unidir_er.append(np.array(n_p_infinities).mean(axis=0))

        if bidir:
            # 2.2 make ps to psk
            self.psk_bidir = [element * self.average_degree for element in self.remaining_nodes_options]

            # 3. Draw scatter plot
            self.plot_pk_infinity(list(self.p_infinities_inter_bidir_er),
                                  f"Comparison interdependent ER with different N \ner_start_n: "
                                  f"{er_start_n}, er_nr_steps: "
                                  f"{er_nr_steps}",
                                  bidir,
                                  "ERInter")
        else:
            # 2.2 make ps to psk
            self.psk_unidir = [element * self.average_degree for element in self.remaining_nodes_options]

            # 3. Draw scatter plot
            self.plot_pk_infinity(list(self.p_infinities_inter_unidir_er),
                                  f"Comparison interdependent ER with different N \ner_start_n: "
                                  f"{er_start_n}, er_nr_steps: "
                                  f"{er_nr_steps}",
                                  bidir,
                                  "ERInter")

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

        # 2.2 make ps to psk
        self.psk_reg = [element * self.average_degree for element in self.remaining_nodes_options]

        # 4. Draw scatter plot
        self.plot_pk_infinity(self.p_infinities_reg_er,
                              f"Comparison regular ER with different N er_start_n: {er_start_n}, er_nr_steps: "
                              f"{er_nr_steps}",
                              True,
                              "ERReg")

    def analyse_inter_networks_augmenting_n(self, nr_nodes, bidir):
        # 1. Create Networks
        self.names_part2.append("ER")
        self.names_part2.append("RR")
        self.names_part2.append("SF_2.3")
        self.names_part2.append("SF_2.7")
        self.names_part2.append("SF_3.0")

        start_time = time.time()
        for nw_type in self.nw_types:
            nw_time = time.time()
            print("Simulate network type {}. Time elapsed since start: {}".format(nw_type, nw_time - start_time))
            n_p_infinities = []
            for i in range(self.nr_created_networks):
                print("Network {}: {} out of {} networks created".format(nw_type, i, self.nr_created_networks))
                # 1. Create network
                network = self.create_network(nw_type, nr_nodes, bidir)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(network)
                n_p_infinities.append(p_infinities)
            if bidir:
                self.p_infinities_inter_bidir_ns.append(np.array(n_p_infinities).mean(axis=0))
            else:
                self.p_infinities_inter_unidir_ns.append(np.array(n_p_infinities).mean(axis=0))
        # 3. plot
        if bidir:
            self.plot_p_infinity(self.p_infinities_inter_bidir_ns,
                                 f"Comparison Interdependent Networks with {nr_nodes} Nodes",
                                 bidir,
                                 "NSInter")
        else:
            self.plot_p_infinity(self.p_infinities_inter_unidir_ns,
                                 f"Comparison Interdependent Networks with {nr_nodes} Nodes",
                                 bidir,
                                 "NSInter")

    def analyse_reg_networks_augmenting_n(self, nr_nodes):
        # 1. Create Networks
        self.names_part2.append("ER")
        self.names_part2.append("RR")
        self.names_part2.append("SF_2.3")
        self.names_part2.append("SF_2.7")
        self.names_part2.append("SF_3.0")

        start_time = time.time()
        for nw_type in self.nw_types:
            nw_time = time.time()
            print("Simulate network type {}. Time elapsed since start: {}".format(nw_type, nw_time - start_time))
            n_p_infinities = []
            for i in range(self.nr_created_networks):
                print("Network {}: {} out of {} networks created".format(nw_type, i, self.nr_created_networks))
                # 1. Create network
                network = self.create_network(nw_type, nr_nodes, True, inter=False)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(network, inter=False)
                n_p_infinities.append(p_infinities)
            self.p_infinities_reg_ns.append(np.array(n_p_infinities).mean(axis=0))
        # 3. plot
        self.plot_p_infinity(self.p_infinities_reg_ns,
                             f"Comparison Regular Networks with {nr_nodes} Nodes",
                             True,
                             "NSReg")

    def save_results(self):
        directory = os.path.dirname(__file__)

        if len(self.p_infinities_inter_unidir_er) > 0:
            path = os.path.join(directory, 'results',
                                "resultsInterErUnidir" + str(int(time.time())) + ".csv")
            p_infinities = np.array(self.p_infinities_inter_unidir_er).transpose()
            results = pd.DataFrame(p_infinities, columns=self.ns)
            results['psk'] = self.psk_unidir
            results.to_csv(path)

        if len(self.p_infinities_inter_bidir_er) > 0:
            path = os.path.join(directory, 'results',
                                "resultsInterErBidir" + str(int(time.time())) + ".csv")
            p_infinities = np.array(self.p_infinities_inter_bidir_er).transpose()
            results = pd.DataFrame(p_infinities, columns=self.ns)
            results['psk'] = self.psk_bidir
            results.to_csv(path)

        if len(self.p_infinities_reg_er) > 0:
            path = os.path.join(directory, 'results', "resultsRegEr" + str(int(time.time())) + ".csv")
            p_infinities = np.array(self.p_infinities_reg_er).transpose()
            results = pd.DataFrame(p_infinities, columns=self.ns)
            results['psk'] = self.psk_reg
            results.to_csv(path)

        if len(self.p_infinities_inter_unidir_ns) > 0:
            path = os.path.join(directory, 'results',
                                "resultsInterNetworksUnidir" + str(int(time.time())) + ".csv")
            p_infinities = np.array(self.p_infinities_inter_unidir_ns).transpose()
            results = pd.DataFrame(p_infinities, columns=self.nw_types)
            results['ps'] = self.remaining_nodes_options
            results.to_csv(path)

        if len(self.p_infinities_inter_bidir_ns) > 0:
            path = os.path.join(directory, 'results',
                                "resultsInterNetworksBidir" + str(int(time.time())) + ".csv")
            p_infinities = np.array(self.p_infinities_inter_bidir_ns).transpose()
            results = pd.DataFrame(p_infinities, columns=self.nw_types)
            results['ps'] = self.remaining_nodes_options
            results.to_csv(path)

        if len(self.p_infinities_reg_ns) > 0:
            path = os.path.join(directory, 'results',
                                "resultsRegNetworks" + str(int(time.time())) + ".csv")
            p_infinities = np.array(self.p_infinities_reg_ns).transpose()
            results = pd.DataFrame(p_infinities, columns=self.nw_types)
            results['ps'] = self.remaining_nodes_options
            results.to_csv(path)

        for p_inf_inter_unidir, p_inf_inter_bidir, p_inf_reg, name in zip(self.p_infinities_inter_unidir_ns,
                                                                          self.p_infinities_inter_bidir_ns,
                                                                          self.p_infinities_reg_ns,
                                                                          self.names_part2):
            plt.figure()
            plt.plot(self.remaining_nodes_options, p_inf_inter_unidir, color='red')
            plt.plot(self.remaining_nodes_options, p_inf_inter_bidir, color='green')
            plt.plot(self.remaining_nodes_options, p_inf_reg, color='blue')
            plt.xlabel("p")
            plt.ylabel("P Infinity")
            labels = ["interdependent unidirectional", "interdependen bidirectional", "regular"]
            plt.legend(labels)
            plt.title(f"Comparison Interdependent vs. Regular {name} Networks")
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', str(name) + str(int(time.time())) + ".png")
            plt.savefig(path)

    @staticmethod
    def compare_inter_reg_er(path_inter="", path_reg=""):
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'results')

        if not path_inter:
            path_inter = os.path.join(path, [f for f in os.listdir(path) if "InterEr" in f][0])

        if not path_reg:
            path_reg = os.path.join(path, [f for f in os.listdir(path) if "RegEr" in f][0])

        inter_df = pd.read_csv(path_inter)
        reg_df = pd.read_csv(path_reg)
        ns = inter_df.columns.values.tolist()
        ns.remove("Unnamed: 0")
        ns.remove("psk")

        for p_inf_inter_er, p_inf_reg_er, n in zip(inter_df.loc[:, ~inter_df.columns.isin(['Unnamed: 0', 'psk'])],
                                                   reg_df.loc[:, ~reg_df.columns.isin(['Unnamed: 0', 'psk'])],
                                                   ns):
            plt.figure()
            plt.plot(inter_df["psk"], inter_df[p_inf_inter_er], color='red')
            plt.plot(inter_df["psk"], reg_df[p_inf_reg_er], color='blue')
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular ER network for N = " + str(n), fontsize=9)
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', "compareErInterReg" + str(n) + str(time.time()) + ".png")
            plt.savefig(path)

    @staticmethod
    def compare_inter_reg_part2(path_inter="", path_reg=""):
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'results')

        if not path_inter:
            path_inter = os.path.join(path, [f for f in os.listdir(path) if "InterNetworks" in f][0])

        if not path_reg:
            path_reg = os.path.join(path, [f for f in os.listdir(path) if "RegNetworks" in f][0])

        inter_df = pd.read_csv(path_inter)
        reg_df = pd.read_csv(path_reg)
        names = inter_df.columns.values.tolist()
        names.remove("Unnamed: 0")
        names.remove("ps")

        for p_inf_inter, p_inf_reg, name in zip(inter_df.loc[:, ~inter_df.columns.isin(['Unnamed: 0', 'ps'])],
                                                reg_df.loc[:, ~reg_df.columns.isin(['Unnamed: 0', 'ps'])],
                                                names):
            plt.figure()
            plt.plot(inter_df["ps"], inter_df[p_inf_inter], color='red')
            plt.plot(inter_df["ps"], reg_df[p_inf_reg], color='blue')
            plt.xlabel("p")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular {} Network".format(name), fontsize=9)
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', "compareNetworksInterReg" + str(name) + str(time.time()) + ".png")
            plt.savefig(path)

    @staticmethod
    def compare_uni_bi_networks(path_uni="", path_bi=""):
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'results')

        if not path_uni:
            path_uni = os.path.join(path, [f for f in os.listdir(path) if "NetworksBidirFalse" in f][0])

        if not path_bi:
            path_bi = os.path.join(path, [f for f in os.listdir(path) if "NetworksBidirTrue" in f][0])

        uni_df = pd.read_csv(path_uni)
        bi_df = pd.read_csv(path_bi)
        names = uni_df.columns.values.tolist()
        names.remove("Unnamed: 0")
        names.remove("ps")

        for p_inf_uni, p_inf_bi, name in zip(uni_df.loc[:, ~uni_df.columns.isin(['Unnamed: 0', 'ps'])],
                                             bi_df.loc[:, ~bi_df.columns.isin(['Unnamed: 0', 'ps'])],
                                             names):
            plt.figure()
            plt.plot(uni_df["ps"], uni_df[p_inf_uni], color='red')
            plt.plot(uni_df["ps"], bi_df[p_inf_bi], color='blue')
            plt.xlabel("p")
            plt.ylabel("P Infinity")
            labels = ["unidirectional", "bidirectional"]
            plt.legend(labels)
            plt.title("Comparison Unidirectional vs. Bidirectional {} Networks".format(name), fontsize=9)
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', "compareNetworksUniBi" + str(name) + str(time.time()) + ".png")
            plt.savefig(path)
