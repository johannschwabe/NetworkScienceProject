import matplotlib.pyplot as plt
import os
from ER import ER
from RandomRegular import RandomRegular
from ScaleFree import ScaleFree
import numpy as np
import networkx as nx
import random


class Simulator:

    def __init__(self):
        # params whole analysis
        self.start_n = 100  # defines the number of nodes of the smallest network for er analysis. Then n_new = n * 2^i
        self.number_of_ns = 3  # defines number of networks to create for er analysis
        self.nr_of_runs_network_creation = 3  # defines how often the step of creating a network should be repeated
        self.nr_of_runs_killing = 10  # defines how often the killing should be repeated
        self.average_degree = 4
        self.ps = np.linspace(0.5, 1, 5)  # start point (0 = 0%), end point (1 = 100%) and number of steps to generate

        # params er analysis
        self.ns = []
        self.er_inter_names = []
        self.er_reg_names = []

        self.psk = []
        self.p_infinities_reg_er = []
        self.p_infinities_inter_er = []

        # params second analysis
        self.names_part2 = []
        self.n_part2 = 10
        self.average_degree_part2 = 4
        self.lambdas_part2 = [3, 2.7, 2.3]

        self.p_infinities_inter_part2 = []
        self.p_infinities_reg_part2 = []

    def simulate_killing(self, network, inter=True):
        p_infinities = []
        for p in self.ps:
            gc_exists_list = []
            for m in range(self.nr_of_runs_killing):
                if inter:
                    local_network = network.clone()
                    size = network.nr_nodes
                    nr_to_destroy = int(np.floor(local_network.nr_nodes * (1 - p)))
                    local_network.destroy_nodes(nr_to_destroy)
                    gc_exists_list.append(local_network.p_mu_n(size-nr_to_destroy))
                else:
                    local_network = nx.Graph(network)
                    nr_to_destroy = int(np.floor(len(local_network.nodes) * (1 - p)))
                    for i in range(nr_to_destroy):
                        local_network.remove_node(random.choice(list(local_network.nodes)))
                    # Calculate p infinity
                    connected_components = [len(c) for c in
                                            sorted(nx.connected_components(local_network), key=len, reverse=True)]
                    if connected_components[0] > 1:
                        p_mu = connected_components[0] / len(local_network.nodes)
                    else:
                        p_mu = 0
                    gc_exists_list.append(p_mu)
            p_infinities.append(np.mean(gc_exists_list))
        return p_infinities

    def plot_pk_infinity(self, p_infinities_nw, title):
        plt.figure()
        for p_infinities in p_infinities_nw:
            plt.plot(self.psk, p_infinities)
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")
        plt.title(title)
        plt.legend(self.ns)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures',  str(title) + ".png")
        plt.savefig(path)

    def plot_p_infinity(self, p_infinities_nw, title):
        plt.figure()
        for p_infinities in p_infinities_nw:
            plt.plot(self.ps, p_infinities)
            plt.xlabel("p")
            plt.ylabel("P Infinity")
        plt.title(title)
        plt.legend(self.names_part2)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures', str(title) + ".png")
        plt.savefig(path)

    def analyse_inter_er_augmenting_n(self):

        # Ns from paper 1000, 2000, 4000 ... 64 000
        self.ns = []
        for i in range(0, self.number_of_ns):
            self.ns.append(2**i * self.start_n)

        for n in self.ns:
            n_p_infinities = []
            for i in range(self.nr_of_runs_network_creation):
                # 1. Create interdependent Erdos Renyi networks
                er_network = ER(n, self.average_degree / n)
                er_network.interconnect_bidirectional()
                # 2. Perform cascading failure M times for increasing p to calculate pInfinity
                p_infinities = self.simulate_killing(er_network)
                n_p_infinities.append(p_infinities)
            self.p_infinities_inter_er.append(np.array(n_p_infinities).mean(axis=0))
            self.er_inter_names.append("Interdependent ER Network " + str(self.average_degree) + " " + str(n))
        # self.p_infinities_inter_er = np.array(self.p_infinities_inter_er).mean(axis=0)

        # 2.2 make ps to psk
        self.psk = [element * self.average_degree for element in self.ps]

        # 3. Draw scatter plot
        self.plot_pk_infinity(list(self.p_infinities_inter_er), "Comparison interdependent ER with different N")

    def analyse_reg_er_augmenting_n(self):

        # Ns from paper 1000, 2000, 4000 ... 64 000
        self.ns = []
        for i in range(self.number_of_ns):
            self.ns.append(2 ** i * self.start_n)

        for n in self.ns:
            n_p_infinities = []
            for i in range(self.nr_of_runs_network_creation):
                # 1. Create regular Erdos Renyi networks
                er_network = nx.erdos_renyi_graph(n, self.average_degree / n)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(er_network, inter=False)
                n_p_infinities.append(p_infinities)
            self.p_infinities_reg_er.append(np.array(n_p_infinities).mean(axis=0))
            self.er_reg_names.append("Regular ER Network " + str(self.average_degree) + " " + str(n))

        # 2.2 make ps to psk
        self.psk = [element * self.average_degree for element in self.ps]

        # 4. Draw scatter plot
        self.plot_pk_infinity(self.p_infinities_reg_er, "Comparison regular ER with different N")

    def compare_inter_reg_er(self):
        for p_inf_inter_er, p_inf_reg_er, name, n in zip(self.p_infinities_inter_er, self.p_infinities_reg_er, self.er_inter_names, self.ns):
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

    def create_network(self, nw_type, param, inter=True):
        if inter:
            if nw_type == "ER":
                network = ER(param[0], param[1] / param[0])
            elif nw_type == "RR":
                network = RandomRegular(param[0], param[1])
            elif nw_type == "SF":
                network = ScaleFree(param[0], param[1], param[2])
        else:
            if nw_type == "ER":
                network = nx.erdos_renyi_graph(param[0], (param[1] / param[0]))
            elif nw_type == "RR":
                network = nx.random_regular_graph(param[1], param[0])
            elif nw_type == "SF":
                sequence1 = nx.utils.powerlaw_sequence(param[0], param[1])
                avg = np.average(sequence1)
                new_seq_1 = np.array(np.round(np.array(sequence1) * param[2] / avg), dtype=int)
                if np.sum(new_seq_1) % 2 == 1:
                    new_seq_1[0] += 1
                network = nx.configuration_model(new_seq_1)
        return network

    def analyse_inter_networks_augmenting_n(self):

        # 1. Create Networks
        network_types = ["ER", "RR", "SF", "SF", "SF"]
        network_params = [[self.n_part2, self.average_degree_part2],
                          [self.n_part2, self.average_degree_part2],
                          [self.n_part2, self.lambdas_part2[0], self.average_degree_part2],
                          [self.n_part2, self.lambdas_part2[1], self.average_degree_part2],
                          [self.n_part2, self.lambdas_part2[2], self.average_degree_part2]]

        self.names_part2.append("ER")
        self.names_part2.append("RR")
        self.names_part2.append("SF lam = " + str(self.lambdas_part2[0]))
        self.names_part2.append("SF lam = " + str(self.lambdas_part2[1]))
        self.names_part2.append("SF lam = " + str(self.lambdas_part2[2]))

        for nw_type, nw_param in zip(network_types, network_params):
            n_p_infinities = []
            for i in range(self.nr_of_runs_network_creation):
                # 1. Create network
                network = self.create_network(nw_type, nw_param)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(network)
                n_p_infinities.append(p_infinities)
            self.p_infinities_inter_part2.append(np.array(n_p_infinities).mean(axis=0))
        # 3. plot
        self.plot_p_infinity(self.p_infinities_inter_part2, "Comparison Interdependent Networks")

    def analyse_reg_networks_augmenting_n(self):
        # 1. Create Networks
        network_types = ["ER", "RR", "SF", "SF", "SF"]
        network_params = [[self.n_part2, self.average_degree_part2],
                          [self.n_part2, self.average_degree_part2],
                          [self.n_part2, self.lambdas_part2[0], self.average_degree_part2],
                          [self.n_part2, self.lambdas_part2[1], self.average_degree_part2],
                          [self.n_part2, self.lambdas_part2[2], self.average_degree_part2]]

        self.names_part2.append("ER")
        self.names_part2.append("RR")
        self.names_part2.append("SF lam = " + str(self.lambdas_part2[0]))
        self.names_part2.append("SF lam = " + str(self.lambdas_part2[1]))
        self.names_part2.append("SF lam = " + str(self.lambdas_part2[2]))

        for nw_type, nw_param in zip(network_types, network_params):
            n_p_infinities = []
            for i in range(self.nr_of_runs_network_creation):
                # 1. Create network
                network = self.create_network(nw_type, nw_param, False)
                # 3. Perform killing of nodes
                p_infinities = self.simulate_killing(network, inter=False)
                n_p_infinities.append(p_infinities)
            self.p_infinities_reg_part2.append(np.array(n_p_infinities).mean(axis=0))
        # 3. plot
        self.plot_p_infinity(self.p_infinities_reg_part2, "Comparison Regular Networks")

    def compare_inter_reg_part2(self):
        for p_inf_inter, p_inf_reg, name in zip(self.p_infinities_inter_part2, self.p_infinities_reg_part2, self.names_part2):
            plt.figure()
            plt.plot(self.ps, p_inf_inter, color='red')
            plt.plot(self.ps, p_inf_reg, color='blue')
            plt.xlabel("p")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular {} Network".format(name))
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', str(name) + ".png")
            plt.savefig(path)


sim = Simulator()
sim.analyse_inter_networks_augmenting_n()
sim.analyse_reg_networks_augmenting_n()
sim.compare_inter_reg_part2()
