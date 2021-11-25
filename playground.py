from Simulator import Simulator
from InterdependantNetwork import InterdependantNetwork

neti = InterdependantNetwork("ER", 20, 20)
sim = Simulator(neti)
sim.simulate()