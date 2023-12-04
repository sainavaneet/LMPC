import pandas as pd
import numpy as np

# Load the data
leader_data = pd.read_csv('iteration_10_data.csv')
follower_data = pd.read_csv('H2_values.csv')

# Ensure both dataframes have the same length
min_length = min(len(leader_data), len(follower_data))
leader_data = leader_data.iloc[:min_length]
follower_data = follower_data.iloc[:min_length]

# Calculate MSE for X, Y, Theta
mse_x = np.mean((leader_data['X'] - follower_data['X'])**2)
mse_y = np.mean((leader_data['Y'] - follower_data['Y'])**2)
mse_theta = np.mean((leader_data['Theta'] - follower_data['Theta'])**2)

# Calculate overall MSE
overall_mse = (mse_x + mse_y + mse_theta) / 3

print("MSE for X: ", mse_x)
print("MSE for Y: ", mse_y)
print("MSE for Theta: ", mse_theta)
print("Overall MSE: ", overall_mse)
