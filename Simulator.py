import matplotlib.pyplot as plt
import os
from ER import ER
from InterdependantNetwork import InterdependantNetwork
from RandomRegular import RandomRegular
from ScaleFree import ScaleFree
import numpy as np
import networkx as nx
import scipy as sp
import random


class Simulator:

    def __init__(self):
        # params er analysis
        self.number_of_ns = 2
        self.number_of_runs_er = 10
        self.er_average_degree = 4
        self.er_inter_names = []
        self.er_reg_names = []
        self.ps = []
        self.p_infinities_reg_er = []
        self.p_infinities_inter_er = []
        self.psk = []
        self.ns = []

        # params second analysis
        self.inter_networks = []
        self.names_part2 = []
        self.reg_networks = []
        self.n_part2 = 50
        self.average_degree_part2 = 4
        self.lambdas_part2 = [3, 2.7, 2.3]

        self.p_infinities_inter_part2 = []
        self.p_infinities_reg_part2 = []

    def simulate(self):
        # nr_nodes = 50000
        nr_nodes = 10
        average_degree = 4
        networks = [
            ER(nr_nodes, nr_nodes, average_degree/nr_nodes, average_degree/nr_nodes),
            RandomRegular(nr_nodes, nr_nodes, average_degree, average_degree),
            ScaleFree(nr_nodes, nr_nodes, 3.0, 3.0, average_degree, average_degree),
            ScaleFree(nr_nodes, nr_nodes, 2.7, 2.7, average_degree, average_degree),
            ScaleFree(nr_nodes, nr_nodes, 2.3, 2.3, average_degree, average_degree),
                    ]
        to_return = {}
        testrange = 0
        for neti in networks:
            neti.interconnect_bidirectional(nr_nodes)

            print(str(neti))
            res = []
            for i in range(testrange, 100):
                local_neti = neti.clone()
                to_remove = int(((100 - i) / 100) * nr_nodes)
                local_neti.destroy_nodes(to_remove, to_remove)
                res.append((len(local_neti.graph_1.nodes) + len(local_neti.graph_2.nodes))/(nr_nodes * 2))
            to_return[str(neti)] = res
        plt.figure()
        for neti_name, netter in to_return.items():
            plt.plot(range(testrange, 100), netter, label=neti_name)
        plt.legend(self.ns)
        plt.show()

        return to_return

    def simulate_killing(self, networks, nr_of_runs, inter=True):
        ps = []
        networks_p_infinities = []
        for network in networks:
            p_infinities = []
            pss = []
            for p in range(1, 100):
                gc_exists_list = []
                for m in range(1, nr_of_runs):
                    if inter:
                        local_network = network.clone()
                        nr_to_destroy = int(np.floor(local_network.nr_nodes_1 * (1 - 0.01 * p)))
                        local_network.destroy_nodes(nr_to_destroy, nr_to_destroy)
                        gc_exists_list.append(local_network.p_mu_n())
                    else:
                        local_network = nx.Graph(network)
                        nr_to_destroy = int(np.floor(len(local_network.nodes) * (1 - 0.01 * p)))
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
                pss.append(p)
                p_infinities.append(np.mean(gc_exists_list))
            ps.append(pss)
            networks_p_infinities.append(p_infinities)
            self.ps = ps
            self.p_infinities_inter_er = networks_p_infinities
        return ps, networks_p_infinities

    def plot_pk_infinity(self, psk, network_p_infinities, title):
        plt.figure()
        for p_infinities, pss in zip(network_p_infinities, psk):
            plt.plot(pss, p_infinities)
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")
        plt.title(title)
        plt.legend(self.ns)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures',  str(title) + ".png")
        plt.savefig(path)

    def plot_p_infinity(self, ps, network_p_infinities, title):
        plt.figure()
        for p_infinities, pss in zip(network_p_infinities, ps):
            plt.plot(pss, p_infinities)
            plt.xlabel("p")
            plt.ylabel("P Infinity")
        plt.title(title)
        plt.legend(self.names_part2)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'figures', str(title) + ".png")
        plt.savefig(path)

    def set_params_er_analysis(self, number_of_ns, number_of_runs_er, er_average_degree):
        self.number_of_ns = number_of_ns
        self.number_of_runs_er = number_of_runs_er
        self.er_average_degree = er_average_degree

    def analyse_interdependent_er_augmenting_n(self):
        ns = []
        # Ns from paper 1000, 2000, 4000 ... 64 000
        for i in range(0, self.number_of_ns):
            ns.append(2**i * 10)
        self.ns = ns

        # 1. Create interdependent Erdos Renyi networks
        er_networks = []
        for n in ns:
            er_network = ER(n, n, self.er_average_degree / n, self.er_average_degree / n)
            er_network.interconnect_bidirectional(n)
            er_networks.append(er_network)
            self.er_inter_names.append("Interdependent ER Network " + str(self.er_average_degree) + " " + str(n))

        # 2. Perform cascading failure M times for increasing p to calculate pInfinity
        ps, networks_p_infinities = self.simulate_killing(er_networks, self.number_of_runs_er)

        # 2.2 make ps to psk
        psk = []
        for pss in ps:
            psk.append([element * self.er_average_degree*0.01 for element in pss])

        # 3. Draw scatter plot
        self.plot_pk_infinity(psk, networks_p_infinities, "Comparison interdependent ER with different N")

    def analyse_regular_er_augmenting_n(self):
        ns = []
        # Ns from paper 1000, 2000, 4000 ... 64 000
        for i in range(self.number_of_ns):
            ns.append(2 ** i * 10)

        # 1. Create regular Erdos Renyi networks
        er_networks = []
        for n in ns:
            er_network = nx.erdos_renyi_graph(n, self.er_average_degree / n)
            er_networks.append(er_network)
            self.er_reg_names.append("Regular ER Network " + str( self.er_average_degree) + " " + str(n))

        # 3. Perform killing of nodes
        ps, networks_p_infinities = self.simulate_killing(er_networks, self.number_of_runs_er, inter=False)

        # 3.2 make ps to psk
        self.psk = []
        for pss in ps:
            self.psk.append([element * self.er_average_degree * 0.01 for element in pss])

        # 4. Draw scatter plot
        self.plot_pk_infinity(self.psk, networks_p_infinities, "Comparison regular ER with different N")

    def compare_regular_interdependent_er(self):
        for p_inf_inter_er, p_inf_reg_er, pss, name, n in zip(self.p_infinities_inter_er, self.p_infinities_reg_er, self.psk, self.er_inter_names, self.ns):
            plt.figure()
            plt.plot(pss, p_inf_inter_er, color='red')
            plt.plot(pss, p_inf_reg_er, color='blue')
            plt.xlabel("p<k>")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular ER network for N = " + str(n))
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', str(name) + ".png")
            plt.savefig(path)

    def analyse_inter_networks_augmenting_n(self):
        # 1. Create Networks
        self.inter_networks = []
        self.names_part2 = []

        # ER Network
        self.inter_networks.append(ER(self.n_part2,
                                      self.n_part2,
                                      self.average_degree_part2 / self.n_part2,
                                      self.average_degree_part2 / self.n_part2))
        self.names_part2.append("ER")
        # Random Regular Network
        self.inter_networks.append(RandomRegular(self.n_part2,
                                                 self.n_part2,
                                                 self.average_degree_part2,
                                                 self.average_degree_part2))
        self.names_part2.append("RR")
        # Scale Free Networks
        for lam in self.lambdas_part2:
            self.inter_networks.append(ScaleFree(self.n_part2, self.n_part2,
                                                 lam, lam,
                                                 self.average_degree_part2, self.average_degree_part2))
            self.names_part2.append("SF lam = " + str(lam))

        for network in self.inter_networks:
            network.interconnect_bidirectional(self.n_part2)

        # 2. Perform killing and calculate P infinity
        ps, networks_p_infinities = self.simulate_killing(self.inter_networks, self.number_of_runs_er)
        self.p_infinities_inter_part2 = networks_p_infinities
        # 3. plot
        self.plot_p_infinity(ps, networks_p_infinities, "Comparison Interdependent Networks")

    def analyse_reg_networks_augmenting_n(self):
        # 1. Create Networks
        self.reg_networks = []
        self.names_part2 = []

        # ER Network
        self.reg_networks.append(nx.erdos_renyi_graph(self.n_part2, self.average_degree_part2 / self.n_part2))
        self.names_part2.append("ER")

        # Random Regular Network
        self.reg_networks.append(nx.random_regular_graph(self.average_degree_part2, self.n_part2))
        self.names_part2.append("RR")

        # Scale Free Networks
        for lam in self.lambdas_part2:
            sequence1 = nx.utils.powerlaw_sequence(self.n_part2, lam)
            avg = np.average(sequence1)
            new_seq_1 = np.array(np.round(sequence1 * self.average_degree_part2 / avg), dtype=int)
            if np.sum(new_seq_1) % 2 == 1:
                new_seq_1[0] += 1
            self.reg_networks.append(nx.configuration_model(new_seq_1))
            self.names_part2.append("SF lam = " + str(lam))

        # 2. Perform killing and calculate P infinity
        ps, networks_p_infinities = self.simulate_killing(self.reg_networks, self.number_of_runs_er, inter=False)
        self.p_infinities_reg_part2 = networks_p_infinities
        # 3. plot
        self.plot_p_infinity(ps, networks_p_infinities, "Comparison Regular Networks")

    def comparison_inter_reg_part2(self):
        for p_inf_inter, p_inf_reg, pss, name in zip(self.p_infinities_inter_part2, self.p_infinities_reg_part2, self.ps, self.names_part2):
            plt.figure()
            plt.plot(pss, p_inf_inter, color='red')
            plt.plot(pss, p_inf_reg, color='blue')
            plt.xlabel("p")
            plt.ylabel("P Infinity")
            labels = ["interdependent", "regular"]
            plt.legend(labels)
            plt.title("Comparison Interdependent vs. Regular {} Network".format(name))
            directory = os.path.dirname(__file__)
            path = os.path.join(directory, 'figures', str(name) + ".png")
            plt.savefig(path)


# The actual analysis

sim = Simulator()
# sim.analyse_interdependent_er_augmenting_n()
# sim.analyse_regular_er_augmenting_n()
# sim.compare_regular_interdependent_er()
sim.analyse_inter_networks_augmenting_n()
sim.analyse_reg_networks_augmenting_n()
sim.comparison_inter_reg_part2()



