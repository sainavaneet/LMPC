import pandas as pd
import numpy as np

leader_data = pd.read_csv('robot_state_history_graph.csv')

time_step = 0.1

gain_matrix = np.array([[0.4662,  0.2978 , 0.2067], [0.8341, 1.2165, 1.3492]])
Q = np.diag([1 , 1, 1])
R = np.diag([0.1 , 0.1])

follower_state = np.array([0, 0, 0])

def calculate_error(leader_state, follower_state):
    x_leader, y_leader, theta_leader = leader_state
    x_follower, y_follower, theta_follower = follower_state
    x_error = x_leader - x_follower
    y_error = y_leader - y_follower
    theta_error = theta_leader - theta_follower
    return np.array([x_error, y_error, theta_error])

def update_state(state, v, w, dt):
    x, y, theta = state
    x_new = x + v * np.cos(theta) * dt
    y_new = y + v * np.sin(theta) * dt
    theta_new = theta + w * dt  
    return np.array([x_new, y_new, theta_new])

states = []
total_quadratic_cost = 0
current_time = 0.0  # Initialize time

for index, row in leader_data.iterrows():
    if index % 10 == 0:
        leader_state = np.array([row['X'], row['Y'], row['Theta']])
        error = calculate_error(leader_state, follower_state)
        control_input = gain_matrix @ error
        v, w = control_input[0], control_input[1]
        v = abs(v)
        quadratic_cost = error.T @ Q @ error + control_input.T @ R @ control_input
        total_quadratic_cost += quadratic_cost
        follower_state = update_state(follower_state, v, w, time_step)

        # Convert current_time and quadratic_cost to array and concatenate
        state_with_control = np.concatenate(([current_time], follower_state, [v, w, quadratic_cost]))
        states.append(state_with_control)

        current_time += time_step  # Update time
    if index * time_step >= 99.9:
        break

states_df = pd.DataFrame(states, columns=['Time', 'X', 'Y', 'Theta', 'linear', 'angular', 'cost'])
states_df.to_csv('H2_values.csv', index=False)

print(f"Total Quadratic Cost: {total_quadratic_cost}")