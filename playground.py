import sys

from matplotlib import pyplot as plt
import numpy as np

from ScaleFree import ScaleFree
from Simulator import Simulator

nr_created_networks = 5
nr_runs_per_network = 2
range_start = 0.55
range_end = 0.9
range_steps = 20
bidirectional = True

nr_nodes = 50000

er_start_n = 400
er_nr_steps = 6

sim = Simulator(nr_created_networks, nr_runs_per_network, range_start, range_end, range_steps, bidirectional)

#
# sim.analyse_inter_er_augmenting_n(er_start_n, er_nr_steps)
# sim.analyse_reg_er_augmenting_n(er_start_n, er_nr_steps)
sim.analyse_inter_networks_augmenting_n(nr_nodes)
# # sim.analyse_reg_networks_augmenting_n(nr_nodes)
#
# sim.save_results(",".join(sys.argv))
