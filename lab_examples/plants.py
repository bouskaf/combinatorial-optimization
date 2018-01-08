#!/usr/bin/env python3
import gurobipy as gb
import matplotlib.pyplot as plt
import numpy as np

__author__ = 'istvan'

d = [5, 5, 5, 5, 5, 10, 10, 15, 20, 20, 30, 30, 40, 50, 60, 60, 60, 50, 40, 30, 30, 20, 10, 5]
T = len(d)

n_base = 10
e_base = 7
c_base = 2.0 / 24.0

n_peak = 40
e_peak = 2
c_peak = 12

s_max = 100

gamma = 0.75

m = gb.Model()

# The number of running base load power plants.
base = m.addVar(0, n_base, 0, gb.GRB.INTEGER);

# How many peaking power plants are running in each hour.
peak = [m.addVar(0, n_peak, 0, gb.GRB.INTEGER) for t in range(T)]

# Energy storage state in each hour.
s = [m.addVar(0, s_max, 0, gb.GRB.CONTINUOUS) for t in range(T+1)]

# Amount of energy taken from the storage.
a_take = [m.addVar(0, gb.GRB.INFINITY, 0, gb.GRB.CONTINUOUS) for t in range(T)]

# Amount of energy put into the storage.
a_put = [m.addVar(0, gb.GRB.INFINITY, 0, gb.GRB.CONTINUOUS) for t in range(T)]

# Whether we are putting or taking from the storage.
y = [m.addVar(0, 1, 0, gb.GRB.INTEGER) for t in range(T)]

# Amount of generated energy.
g = [m.addVar(0, gb.GRB.INFINITY, 0, gb.GRB.CONTINUOUS) for t in range(T)]

m.update()

for t in range(T):
    m.addConstr(e_base * base + e_peak * peak[t] == g[t])

for t in range(T):
    m.addConstr(g[t] + gamma * a_take[t] - a_put[t] == d[t])

m.addConstr(s[0] == 0)
for t in range(T):
    m.addConstr(s[t + 1] == (s[t] - a_take[t]) + a_put[t])

big_m = s_max
for t in range(T):
    m.addConstr(big_m * (1 - y[t]) >= a_take[t])
    m.addConstr(big_m * y[t] >= a_put[t])

m.setObjective(24 * c_base * base + gb.quicksum([c_peak * peak[t] for t in range(T)]), gb.GRB.MINIMIZE)

m.optimize()

y_lim_max = max(s_max, max([g[t].x + a_take[t].x for t in range(T)])) * 1.1

# Demand plot.
margin = 0.2
width = 0.3
plt.figure(figsize=(10, 4))
plt.bar([t + margin for t in range(T)], d, width=width, color='yellow')

bottom = np.zeros(T)
g_base = np.array([e_base * base.x for t in range(T)])
plt.bar([t + margin + width for t in range(T)],
        g_base,
        width=width,
        bottom=bottom,
        color='red')
bottom += g_base

g_peak = np.array([e_peak * peak[t].x for t in range(T)])
plt.bar([t + margin + width for t in range(T)],
        g_peak,
        width=width,
        bottom=bottom,
        color='green')
bottom += g_peak

g_a_take = np.array([gamma * a_take[t].x for t in range(T)])
plt.bar([t + margin + width for t in range(T)],
        g_a_take,
        width=width,
        bottom=bottom,
        color='blue')
bottom += g_a_take

plt.xlabel("hour")
plt.ylabel("energy")
plt.legend(['demand', 'base', 'peak', 'storage'], ncol=1, loc=2)
plt.xlim(0, 24)
plt.ylim(0, y_lim_max)
plt.xticks(range(24), [i % 24 for i in range(24)])
plt.grid()
plt.savefig('../demand.eps', bbox_inches='tight')

# Storage plot.
plt.figure(figsize=(10, 4))
plt.xlim(0, 24)
plt.xticks(range(24), [i % 24 for i in range(24)])
plt.xlabel("hour")
plt.ylabel("stored energy")
plt.ylim(0, y_lim_max)
plt.bar([t + margin for t in range(T)], [s[t].x for t in range(T)], width=width, color='purple')
plt.grid()
plt.savefig('../storage.eps', bbox_inches='tight')

plt.show()
