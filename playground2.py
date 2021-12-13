from Simulator import Simulator

nr_created_networks = 2
nr_runs_per_network = 2
range_start = 0.1
range_end = 0.5
range_steps = 9

nr_nodes = 50000

er_start_n = 1000
er_nr_steps = 7

sim = Simulator(nr_created_networks, nr_runs_per_network, range_start, range_end, range_steps)

# ER
# sim.analyse_inter_er_augmenting_n(er_start_n, er_nr_steps, True)
# sim.analyse_inter_er_augmenting_n(er_start_n, er_nr_steps, False)
sim.analyse_reg_er_augmenting_n(er_start_n, er_nr_steps)

# NS
# sim.analyse_inter_networks_augmenting_n(nr_nodes, True)
# sim.analyse_inter_networks_augmenting_n(nr_nodes, False)
sim.analyse_reg_networks_augmenting_n(nr_nodes)

sim.save_results()
