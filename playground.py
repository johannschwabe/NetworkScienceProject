import matplotlib.pyplot as plt
import networkx as nx

from RandomRegular import RandomRegular
from ER import ER
from ScaleFree import ScaleFree
from ConfigurationModel import ConfigurationModel
from Simulator import Simulator

simi = Simulator()
print(simi.simulate())

# scali = ScaleFree(1000, 1000, 3, 3, 4, 4)
# scali.destroy_nodes(20, 20)
