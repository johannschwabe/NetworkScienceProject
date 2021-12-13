import matplotlib.pyplot as plt
import pandas as pd

file_path = "results/resultsInterErBidir94399.csv"

dataframe = pd.read_csv(file_path)

plt.figure()
for col in dataframe.columns[1:-1]:
    plt.plot(dataframe[dataframe.columns[-1]], dataframe[col], label=col)

plt.legend()

# Title
plt.title("Interdependent Erdos Renyi networks", fontsize=9)

# x-axes
plt.xlim(0.0, 4.0)
plt.xlabel("p<k>")
# plt.xlim(0.0, 1.0)
# plt.xlabel("p")

# y-axes
plt.ylim(0.0, 1.0)
plt.ylabel("P Infinity")

plt.show()
