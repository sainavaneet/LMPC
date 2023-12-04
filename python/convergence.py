import pandas as pd
import numpy as np

# Load the data
leader_data = pd.read_csv('robot_state_history_graph.csv')
follower_data = pd.read_csv('/home/navaneet/Desktop/ilcmpc/H2_values.csv')


min_length = min(len(leader_data), len(follower_data))
leader_data = leader_data.iloc[:min_length]
follower_data = follower_data.iloc[:min_length]


threshold = 0  # This is an example value; adjust as needed


mse_values = ((leader_data['X'] - follower_data['X'])**2 +
              (leader_data['Y'] - follower_data['Y'])**2 +
              (leader_data['Theta'] - follower_data['Theta'])**2) / 3

# Find the time of convergence
convergence_time = None
for i in range(len(mse_values)):
    if mse_values.iloc[i] < threshold:
        convergence_time = leader_data['Time'].iloc[i]  # Assuming a 'Time' column exists
        break

if convergence_time is not None:
    print("Convergence Time: ", convergence_time)
else:
    print("The follower did not converge to the leader within the threshold.")
