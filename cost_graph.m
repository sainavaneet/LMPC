df1 = readtable('data/H2_values.csv');
df10 = readtable('data/iteration_10_data.csv');


linear1 = df1.linear;
angular1 = df1.angular;
time1 = df1.Time;
cost1 = df1.cost;


X10 = df10.X;
Y10 = df10.Y;
Theta10 = df10.Theta;
linear10 = df10.linear;
angular10 = df10.angular;
time10 = df10.time;
cost10 = df10.cost;

figure;
ax1 = subplot(1, 1, 1); 
stairs(ax1, time1, cost1, 'LineStyle', '--', 'LineWidth', 1, 'Color', 'red');
hold on;
stairs(ax1, time10, cost10, 'LineStyle', '--', 'LineWidth', 1, 'Color', 'blue');
hold off;

% Set labels and title
ylabel(ax1, 'Cost');
xlabel(ax1, 'Time (s)');
title(ax1, 'Cost Comparision');
legend(ax1, 'H2', 'LMPC');

grid(ax1, 'on');


sgtitle('Plot Title'); 