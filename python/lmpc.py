import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import csv

class Controller:
    def __init__(self):
        # Initialization parameters
        self.robot_x, self.robot_y, self.robot_theta = 0.0, 0.0, 0.0
        self.target_x, self.target_y, self.target_theta = 0.0, 0.0, 0.0
        self.current_state = [self.robot_x, self.robot_y, self.robot_theta]
        self.robot_positions = [(self.robot_x, self.robot_y, 0)]
        self.error_history = []
        self.u2_past = None
        self.error_past = np.zeros(3)
        self.cumulative_cost = 0
        self.learning_rate = 5
        self.convergence_threshold = 0
        self.iteration_count = 0
        self.total_iterations = 10
        self.previous_total_cost = 0
        self.gain_matrix = np.array([[0.4662,  0.2978 , 0.2067], [0.8341, 1.2165, 1.3492]])
        

        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.suptitle('Robot Trajectory', fontsize=16)
        
        self.Q = np.diag([1, 1, 1]) 
        self.R = np.diag([0.1, 0.1])   
        
        

    def robot_model(self, state, control_input, dt):
        # Robot dynamics model
        x, y, theta = state
        v, omega = control_input
        x_next = x + v * np.cos(theta) * dt
        y_next = y + v * np.sin(theta) * dt
        theta_next = theta + omega * dt
        return np.array([x_next, y_next, theta_next])

    def calculate_error(self):
        error_x = self.robot_x - self.target_x
        error_y = self.robot_y - self.target_y
        return np.array([error_x, error_y])

    def update_ilc(self, u_optimal, error_current):
        if self.u2_past is not None:
            u_ilc = u_optimal + self.learning_rate * (error_current - self.error_past[:2]) 
            # print(u_ilc)
        else:
            u_ilc = u_optimal
        self.u2_past = u_optimal
        self.error_past = np.append(error_current, self.robot_theta - self.target_theta)  
        return u_ilc

    def plot_positions(self):
        self.ax.clear()
        self.ax.plot3D(*zip(*self.robot_positions), label='Robot Path', c='r', linewidth=1, marker='o', markersize=1)
        self.ax.scatter(self.target_x, self.target_y, self.target_theta, label='Target', c='g', marker='x')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Theta')

        self.ax.legend()
        plt.pause(0.01)

    # def target_cost_function(self, u, *args):
    #     current_state, T = args
    #     N = len(u) // 2
    #     x = current_state.copy()
    #     cost = 0

    #     position_weight, orientation_weight, control_weight = 100, 40, 10

    #     for k in range(N):
    #         control = u[2 * k:2 * k + 2]
    #         theta = x[2]
    #         x[0] += control[0] * np.cos(theta) * T
    #         x[1] += control[0] * np.sin(theta) * T
    #         x[2] += control[1] * T

    #         position_error = np.sqrt((x[0] - self.target_x)**2 + (x[1] - self.target_y)**2)
    #         orientation_error = x[2] - self.target_theta
    #         orientation_error = np.arctan2(np.sin(orientation_error), np.cos(orientation_error))

    #         control_effort = np.sum(np.square(control))

    #         cost += position_weight * position_error**2
    #         cost += orientation_weight * orientation_error**2
    #         cost += control_weight * control_effort

    #     return cost 
    
    def target_cost_function(self, u, *args):
        current_state, T = args
        N = len(u) // 2
        x = current_state.copy()
        cost = 0

        for k in range(N):
            control = u[2 * k:2 * k + 2]
            theta = x[2]
            x[0] += control[0] * np.cos(theta) * T 
            x[1] += control[0] * np.sin(theta) * T 
            x[2] += control[1] * T

            # Quadratic cost terms
            # state_error = np.array([x[0] - self.target_x, x[1] - self.target_y, x[2] - self.target_theta])
            state_error = np.array([self.target_x - x[0],self.target_y - x[1],self.target_theta - x[2]])
            
            cost += state_error.T @ self.Q @ state_error  
            cost += control.T @ self.R @ control          

        return cost  

    def calculate_mpc_control_input(self):
        N, u_dim = 2, 2
        T = 0.1
        v_max, v_min, omega_max = 0.3, 0.0, np.pi/4
        u0 = np.zeros(N * u_dim)
        bounds = [(v_min, v_max) if i % u_dim == 0 else (-omega_max, omega_max) for i in range(N * u_dim)]

        best_u = None
        best_cost = np.inf

        
        args = (self.current_state, T)
        result = minimize(self.target_cost_function, u0, args=args, method='L-BFGS-B', bounds=bounds)

        if result.success and result.fun < best_cost:
            best_cost = result.fun
            best_u = result.x[:u_dim]

        return best_u
    

    
    def load_trajectory(self, file_path, sampling_time=0.1):
        # Load trajectory with new sampling time
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Downsample the trajectory to match the new sampling time
            self.trajectory = [(float(row[0]), float(row[1]), float(row[2])) 
                            for i, row in enumerate(reader) if i % int(sampling_time/0.01) == 0]


    def lmpc_follower(self):
        dt = 0.1
        d_t = 0.1
        self.load_trajectory('robot_state_history.csv')  # Load the trajectory

        with open('cost.csv', mode='w', newline='') as file, \
            open('iteration_1_data.csv', mode='w', newline='') as file_1, \
            open('iteration_10_data.csv', mode='w', newline='') as file_10 , \
            open('iteration_5_data.csv', mode='w', newline='') as file_5:
                
            writer = csv.writer(file)
            writer.writerow(['Iteration', 'cost'])

            writer_1 = csv.writer(file_1)
            writer_1.writerow(['X', 'Y', 'Theta','linear', 'angular', 'time'])
            
            writer_10 = csv.writer(file_10)
            writer_10.writerow(['X', 'Y', 'Theta','linear', 'angular', 'time' , 'cost'])
            writer_5 = csv.writer(file_5)
            writer_5.writerow(['X', 'Y', 'Theta','linear', 'angular', 'time'])

            for iteration in range(self.total_iterations):
                iteration_cost = 0  
                self.reset_for_new_iteration()
                time_elapsed = 0
                iteration_cost_10 = 0
                for target_x, target_y, target_theta in self.trajectory:
                    self.target_x, self.target_y, self.target_theta = target_x, target_y, target_theta

                    error_current = self.calculate_error()
                    self.error_history.append(error_current)

                    u_optimal = self.calculate_mpc_control_input()
                    if iteration == 0:
                        # print("entered")
                        u_ilc = u_optimal
                        writer_1.writerow([self.robot_x, self.robot_y , self.robot_theta , u_ilc[0] , u_ilc[1] , time_elapsed])
                        # u_ilc = self.update_ilc(u_optimal, error_current)
                    else :
                         u_ilc = self.update_ilc(u_optimal, error_current)

                    self.current_state = self.robot_model(self.current_state, u_ilc, dt)
                    self.robot_x, self.robot_y, self.robot_theta = self.current_state
                    self.robot_positions.append((self.robot_x, self.robot_y, self.robot_theta))
                    
                    self.plot_positions()

                    iteration_cost += self.target_cost_function(u_ilc, self.current_state, dt)
                    iteration_cost_10 = self.target_cost_function(u_ilc, self.current_state, dt)
                    
                    if iteration == 9:
                        writer_10.writerow([self.robot_x, self.robot_y , self.robot_theta , u_ilc[0] , u_ilc[1], time_elapsed , iteration_cost_10] )
                        print(iteration_cost_10)
                        
                    if iteration == 5:
                        writer_5.writerow([self.robot_x, self.robot_y , self.robot_theta , u_ilc[0] , u_ilc[1] , time_elapsed])
                        
                    time_elapsed += d_t
                        
                    if np.linalg.norm(error_current) < self.convergence_threshold:
                        break

                    self.iteration_count += 1
                    

                writer.writerow([iteration, iteration_cost])
                print(f"J={iteration + 1} : {iteration_cost}")



    def reset_for_new_iteration(self):
        self.robot_x, self.robot_y, self.robot_theta = 0.0, 0.0, 0.0
        self.current_state = [self.robot_x, self.robot_y, self.robot_theta]
        self.robot_positions = [(self.robot_x, self.robot_y, 0)]
        self.error_history = []
        self.u2_past = None
        self.error_past = np.zeros(3)
        self.iteration_count = 0
        self.learning_rate += 0.1

if __name__ == '__main__':
    try:
        controller = Controller()
        controller.lmpc_follower()
    except KeyboardInterrupt:
        pass
