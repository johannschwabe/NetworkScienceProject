from Simulator import Simulator

nr_created_networks = 2
nr_runs_per_network = 2
range_start = 0.1
range_end = 1.0
range_steps = 10
bidirectional = True

nr_nodes = 1000

er_start_n = 400
er_nr_steps = 6

sim = Simulator(nr_created_networks, nr_runs_per_network, range_start, range_end, range_steps, bidirectional)


sim.analyse_inter_er_augmenting_n(er_start_n, er_nr_steps)
sim.analyse_reg_er_augmenting_n(er_start_n, er_nr_steps)
# sim.analyse_inter_networks_augmenting_n(nr_nodes)
# sim.analyse_reg_networks_augmenting_n(nr_nodes)

sim.save_results()
