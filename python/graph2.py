import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from genpy import Time

# Load the data for iteration 1 and iteration 10
# df1 = pd.read_csv('/home/navaneet/Desktop/ilcmpc/control_history.csv')
df10 = pd.read_csv('/home/navaneet/Desktop/ilcmpc/iteration_10_data.csv')
h2 = pd.read_csv('/home/navaneet/Desktop/ilcmpc/H2_values.csv')


# Extract data for iteration 1
# X1 = df1['X'].to_numpy()
# Y1 = df1['Y'].to_numpy()
# Theta1 = df1['Theta'].to_numpy()
# linear1 = df1['linear'].to_numpy()
# angular1 = df1['angular'].to_numpy()
# Time1 = df1['time'].to_numpy()



X10 = df10['X'].to_numpy()
Y10 = df10['Y'].to_numpy()
Theta10 = df10['Theta'].to_numpy()
linear10 = df10['linear'].to_numpy()
angular10 = df10['angular'].to_numpy()
time10 = df10['time'].to_numpy()

cost10 = df10['cost'].to_numpy()

cost_h2 = h2['cost'].to_numpy()





fig, (ax) = plt.subplots(figsize=(10, 8))

# Plot X, Y, and Theta for iteration 1
ax.step(time10,cost10, label='Lmpc_cost',linestyle ='--',linewidth = 1,color='red')
ax.step(time10,cost_h2, label='H2_cost',linestyle ='--',linewidth = 1,color='blue')
# ax.plot(cost10, label='Lmpc_cost',linestyle ='--',linewidth = 1,color='blue')
# ax.plot(cost_h2, label='H2_cost',linestyle ='--',linewidth = 1,color='red')



# ax.plot(Time1,angular1, label='leader "w"',linestyle =':',linewidth = 1,color='red')

ax.set_ylabel('Cost Value')
ax.set_xlabel('Time(s)')

ax.set_title('cost Comparision ')

ax.legend()



# ax.set_ylim(-0.1, 0.4 ,)

# ax2.set_xlim(0 , 10 , 0.1)




plt.tight_layout()
plt.show()
