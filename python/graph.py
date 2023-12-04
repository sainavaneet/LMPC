import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the data for various iterations
# df1 = pd.read_csv('/home/navaneet/Desktop/ilcmpc/iteration_1_data.csv')
df1 = pd.read_csv('H2_values.csv')

df10 = pd.read_csv('iteration_10_data.csv')
df5 = pd.read_csv('iteration_5_data.csv')

df_leader = pd.read_csv('/home/navaneet/Desktop/ilcmpc/robot_state_history_graph.csv')

# Extract data for each iteration
X1, Y1 , Theta1= df1['X'].to_numpy(), df1['Y'].to_numpy() , df1['Theta'].to_numpy()
X10, Y10 = df10['X'].to_numpy(), df10['Y'].to_numpy()
X5, Y5 = df5['X'].to_numpy(), df5['Y'].to_numpy()
X_l, Y_l , Theta_l = df_leader['X'].to_numpy(), df_leader['Y'].to_numpy() , df_leader['Theta'].to_numpy()

# Create a 3D subplot
fig = plt.figure(figsize=(20, 16))
ax = fig.add_subplot(111, projection='3d')

# Plot trajectories for each iteration
ax.plot(X1, Y1, 0, label='H2', linestyle='--', linewidth=1.5, color='black')
ax.plot(X10, Y10, 0, label='Iteration 10', linestyle='-', linewidth=1.5, color='blue')
# ax.plot(X5, Y5, 0, label='Iteration 5', linestyle='--', linewidth=1, color='green')
ax.plot(X_l, Y_l, 0, label='Feasible Traj', linestyle='-', linewidth=1, color='red')  

# Setting labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Trajectory Tracking comparison of H2 and LMPC')
ax.legend()


zoom_xlim = [0.0, 0.1]
zoom_ylim = [0.1, 0.3]

# # Create an inset Axes for 2D zoom-in plot
# inset_ax = fig.add_axes([0.7, 0.5, 0.2, 0.2])  # x, y, width, height relative to figure size

# # Plot the same data on the inset Axes
# inset_ax.plot(X1, Y1, linestyle='--', linewidth=1, color='black')
# inset_ax.plot(X10, Y10, linestyle='-', linewidth=1, color='blue')
# inset_ax.plot(X5, Y5, linestyle='--', linewidth=1, color='green')
# inset_ax.plot(X_l, Y_l, linestyle='-', linewidth=1, color='red')

# # Set the limits for the zoom-in area
# inset_ax.set_xlim(zoom_xlim)
# inset_ax.set_ylim(zoom_ylim)

# # Set labels and title for the inset plot if needed
# inset_ax.set_xlabel('X')
# inset_ax.set_ylabel('Y')
# inset_ax.set_title('Zoomed In for j = 5 and j = 10')

plt.show()
