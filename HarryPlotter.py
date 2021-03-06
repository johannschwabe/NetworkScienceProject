import matplotlib.pyplot as plt
import pandas as pd

# file_path = "results/resultsInterErBidir272132.csv"
# file_path = "results/resultsInterErUnidir325310.csv"
# file_path = "results/resultsRegEr146780.csv"
# file_path = "results/resultsRegNetworks161350.csv"
# file_path = "results/resultsInterNetworksBidir420601.csv"
file_path = "results/resultsInterNetworksUnidir454271.csv"

# fig_path = "figures/BidirER"
# fig_path = "figures/UnidirER"
# fig_path = "figures/RegER"
# fig_path = "figures/RegNS"
# fig_path = "figures/BidirNS"
fig_path = "figures/UnidirNS"

x_min = 0.5
x_max = 0.9

# x_label = "p<k>"
x_label = "p"

dataframe = pd.read_csv(file_path)

plt.figure()
for col in dataframe.columns[1:-1]:
    plt.plot(dataframe[dataframe.columns[-1]], dataframe[col], label=col)

plt.legend()

# Title
# plt.title("Interdependent Bidirectional Erdos Renyi networks", fontsize=9)
# plt.title("Interdependent Bidirectional networks", fontsize=9)
plt.title("Interdependent Unidirectional networks", fontsize=9)
# plt.title("Interdependent Unidirectional Erdos Renyi networks", fontsize=9)
# plt.title("Independent Erdos Renyi networks", fontsize=9)
# plt.title("Independent networks", fontsize=9)

# x-axes
plt.xlim(x_min, x_max)
plt.xlabel(x_label)

# y-axes
plt.ylim(0.0, 1.0)
plt.ylabel("P Infinity")

plt.savefig(fig_path + f"-{x_min}-{x_max}".replace(".", "_") + ".png")
