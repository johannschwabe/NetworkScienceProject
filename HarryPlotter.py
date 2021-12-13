import matplotlib.pyplot as plt
import pandas as pd

# file_path = "results/resultsInterErBidir98299.csv"
# file_path = "results/resultsInterErUnidir98326.csv"
file_path = "results/resultsRegEr92389.csv"

# fig_path = "figures/BidirER"
# fig_path = "figures/UnidirER"
fig_path = "figures/RegER"

x_min = 0.4
x_max = 2.6

x_label = "p<k>"
# x_label = "p"

dataframe = pd.read_csv(file_path)

plt.figure()
for col in dataframe.columns[1:-1]:
    plt.plot(dataframe[dataframe.columns[-1]], dataframe[col], label=col)

plt.legend()

# Title
# plt.title("Interdependent Bidirectional Erdos Renyi networks", fontsize=9)
plt.title("Independent Erdos Renyi networks", fontsize=9)

# x-axes
plt.xlim(x_min, x_max)
plt.xlabel(x_label)
# plt.xlim(0.0, 1.0)
# plt.xlabel("p")

# y-axes
plt.ylim(0.0, 1.0)
plt.ylabel("P Infinity")

plt.savefig(fig_path + f"-{x_min}-{x_max}".replace(".", "_") + ".png")