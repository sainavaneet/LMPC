from math import cos, sin
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Controller:
    
    def __init__(self):
        self.robot_x = 0
        self.robot_y = 0
        self.robot_theta = 0
        self.state_history = []  # To store the history of states
        self.control_history = []  # To store the history of control inputs (v and omega)
        self.time_history = []  # To store the history of time steps

    def wrap_angle(self,angle):
        
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def robot_model(self, state, control_input, dt):
        x, y, theta = state
        v, omega = control_input
        x_next = x + v * np.cos(theta) * dt
        y_next = y + v * np.sin(theta) * dt
        theta_next = theta + omega * dt
        theta_next = self.wrap_angle(theta_next)  
        return np.array([x_next, y_next, theta_next])

    def main(self):
        
        dt = 0.01  
        total_time = 10  

      
        state = np.array([self.robot_x, self.robot_y, self.robot_theta])

        v = 0.1  # constant speed
        segment_time = total_time / 2  

        current_time = 0  

        # First half of 'S'
        omega = np.pi / 5
        for t in np.arange(0, segment_time, dt):
            control_input = np.array([v, omega])
            state = self.robot_model(state, control_input, dt)
            self.state_history.append(state)
            self.control_history.append(control_input)
            self.time_history.append(current_time)
            current_time += dt

        # Second half of 'S'
        omega = -np.pi / 5  # negative angular velocity for the second curve
        for t in np.arange(segment_time, total_time, dt):
            control_input = np.array([v, omega])
            state = self.robot_model(state, control_input, dt)
            self.state_history.append(state)
            self.control_history.append(control_input)
            self.time_history.append(current_time)
            current_time += dt

        combined_state_time = np.column_stack((self.state_history, self.time_history))
        np.savetxt('/home/navaneet/Desktop/ilcmpc/robot_state_history.csv', combined_state_time, delimiter=',', fmt='%0.7f')

        np.savetxt('/home/navaneet/Desktop/ilcmpc/robot_state_history_graph.csv', combined_state_time, delimiter=',' ,header='X,Y,Theta,Time', comments='')

        combined_control_time = np.column_stack((self.control_history, self.time_history))
        np.savetxt('/home/navaneet/Desktop/ilcmpc/control_history.csv', combined_control_time, delimiter=',', header='linear,angular,time', comments='')

        states = np.array(self.state_history)
        x, y, theta = states[:, 0], states[:, 1], states[:, 2]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, theta)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Theta')

        plt.show()

if __name__ == '__main__':
    try:
        controller = Controller()
        controller.main()
    except KeyboardInterrupt:
        pass
