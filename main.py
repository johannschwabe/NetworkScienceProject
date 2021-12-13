from Simulator import Simulator
import sys

if len(sys.argv) != 10:
    raise Exception(f"Wrong number of arguments. {len(sys.argv) - 1} / 9")
nr_created_networks = int(sys.argv[1])
nr_runs_per_network = int(sys.argv[2])
range_start = float(sys.argv[3])
range_end = float(sys.argv[4])
range_steps = int(sys.argv[5])
er_start_n = int(sys.argv[6])
er_nr_steps = int(sys.argv[7])
nr_nodes = int(sys.argv[8])
plot_nr = int(sys.argv[9])

sim = Simulator(nr_created_networks, nr_runs_per_network, range_start, range_end, range_steps)

if plot_nr == 1:
    sim.analyse_inter_er_augmenting_n(er_start_n, er_nr_steps, True)
elif plot_nr == 2:
    sim.analyse_inter_er_augmenting_n(er_start_n, er_nr_steps, False)
elif plot_nr == 3:
    sim.analyse_reg_er_augmenting_n(er_start_n, er_nr_steps)
elif plot_nr == 4:
    sim.analyse_inter_networks_augmenting_n(nr_nodes, True)
elif plot_nr == 5:
    sim.analyse_inter_networks_augmenting_n(nr_nodes, False)
elif plot_nr == 6:
    sim.analyse_reg_networks_augmenting_n(nr_nodes)
else:
    raise Exception("Invalid plot nr.")

sim.save_results()
