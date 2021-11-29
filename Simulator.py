import matplotlib.pyplot as plt

from ER import ER
from InterdependantNetwork import InterdependantNetwork
from RandomRegular import RandomRegular
from ScaleFree import ScaleFree


class Simulator:
    def simulate(self):
        # nr_nodes = 50000
        nr_nodes = 2000
        average_degree = 4
        networks = [
            ER(nr_nodes, nr_nodes, average_degree/nr_nodes, average_degree/nr_nodes),
            RandomRegular(nr_nodes, nr_nodes, average_degree, average_degree),
            ScaleFree(nr_nodes, nr_nodes, 3.0, 3.0, average_degree, average_degree),
            ScaleFree(nr_nodes, nr_nodes, 2.7, 2.7, average_degree, average_degree),
            ScaleFree(nr_nodes, nr_nodes, 2.3, 2.3, average_degree, average_degree),
                    ]
        to_return = []
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
            to_return.append(res)
        plt.figure()
        for netter in to_return:
            plt.plot(range(testrange, 100), netter)
        plt.show()
        return to_return

