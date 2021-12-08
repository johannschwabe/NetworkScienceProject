import time

from Simulator import Simulator

sim = Simulator()
bidirectional = False

# Plt 1
start_er = time.time()
sim.analyse_inter_er_augmenting_n(bidir=bidirectional)
time_er = time.time() - start_er

# Plt 2
start_ns = time.time()
sim.analyse_inter_networks_augmenting_n(bidir=bidirectional)
time_ns = time.time() - start_ns

sim.save_results()

print()
print(f"ER: {time_er}")
print(f"NS: {time_ns}")
