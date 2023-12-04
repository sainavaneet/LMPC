% Load the data for various iterations
df1 = readtable('data/H2_values.csv');
df10 = readtable('data/iteration_10_data.csv');

df_leader = readtable('data/robot_state_history.csv');

% Extract data for each iteration
X1 = df1.X; Y1 = df1.Y; time1 = df1.Time;
X10 = df10.X; Y10 = df10.Y;
X_l = df_leader.X; Y_l = df_leader.Y;

% Create a 3D plot
figure;
ax = axes('NextPlot','add');
view(3);

% Plot trajectories for each iteration
plot3(ax, X1, Y1, zeros(size(X1)), 'LineStyle', '--', 'LineWidth', 1, 'Color', 'black');
plot3(ax, X10, Y10, zeros(size(X10)), 'LineStyle', '-', 'LineWidth', 1, 'Color', 'blue');
plot3(ax, X_l, Y_l, zeros(size(X_l)), 'LineStyle', '-', 'LineWidth', 0.5, 'Color', 'red');

% Setting labels and title
xlabel(ax, 'X');
ylabel(ax, 'Y');
zlabel(ax, 'Z');
title(ax, 'X, Y, and Z for H2 and LMPC');
legend('H2', 'LMPC', 'Feasible Traj');

grid(ax, 'on');

% Make the graph tight
axis(ax, 'tight');
