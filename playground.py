import matplotlib.pyplot as plt
import networkx as nx

from RandomRegular import RandomRegular
from ER import ER
from ScaleFree import ScaleFree
from ConfigurationModel import ConfigurationModel

neti = ConfigurationModel(10, 10, 3, 3)
# neti = ScaleFree(20, 20, 0.41, 0.41, 0.54, 0.54)
# neti = ER(20, 20, 35, 35)
# neti.interconnect_bidirectional(20)
neti.interconnect_unidirectional(2, 2)

neti.destroy_nodes(1, 1)
