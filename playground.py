from Simulator import Simulator
from RandomRegular import RandomRegular

neti = RandomRegular(20, 20, 4, 4)
neti.interconnect(20)
neti.destroy_nodes(1, 1)
