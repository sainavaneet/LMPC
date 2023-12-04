import pandas as pd
import numpy as np


leader_data = pd.read_csv('robot_state_history_graph.csv')
time_step = 0.01  # Sampled time

gain_matrix = np.array([[2.6121, -0.7288, -0.0486], [-0.0459, 1.1225, 2.6765]])

follower_state = np.array([0, 0, 0])


def calculate_error(leader_state, follower_state):
    x_leader, y_leader, theta_leader = leader_state
    x_follower, y_follower, theta_follower = follower_state

    # Error in the global frame
    x_error = x_leader - x_follower
    y_error = y_leader - y_follower
    theta_error = theta_leader - theta_follower
    # print('theta_l = %f, theta_f = %f, theta-error = %f' % (theta_leader, theta_follower, theta_leader - theta_follower))

    return np.array([x_error, y_error, theta_error])

def update_state(state, v, w, dt):
    x, y, theta = state
    x_new = x + v * np.cos(theta) * dt
    y_new = y + v * np.sin(theta) * dt
    theta_new = theta + w * dt  
    return np.array([x_new, y_new, theta_new])


states = []

for index, row in leader_data.iterrows():
    leader_state = np.array([row['X'], row['Y'], row['Theta']])
    error = calculate_error(leader_state, follower_state)

    theta_follower = follower_state[2]

    control_input = gain_matrix @ error
    v, w = control_input[0], control_input[1]

    v = abs(v)

    follower_state = update_state(follower_state, v, w, time_step)

    state_with_control = np.append(follower_state, [v, w])
    states.append(state_with_control)

    if index * time_step >= 9.99:
        break


states_df = pd.DataFrame(states, columns=['X', 'Y', 'Theta', 'linear', 'angular'])
states_df.to_csv('H2_values.csv', index=False)
