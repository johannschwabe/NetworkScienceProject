from RandomRegular import RandomRegular
from ER import ER
from ScaleFree import ScaleFree
from ConfigurationModel import ConfigurationModel

neti = ConfigurationModel(20, 20, 3, 3)
# neti = ScaleFree(20, 20, 0.41, 0.41, 0.54, 0.54)
# neti = ER(20, 20, 35, 35)
neti.interconnect(20)
neti.destroy_nodes(1, 1)
