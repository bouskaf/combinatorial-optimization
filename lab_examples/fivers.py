import gurobipy as g
import matplotlib.pyplot as plt

__author__ = 'tonda'


n = 5 + 2

m = g.Model()

x = {}
y = {}
for i in range(n):
    for j in range(n):
        x[i, j] = m.addVar(vtype=g.GRB.BINARY, obj=1)
        y[i, j] = m.addVar(vtype=g.GRB.INTEGER, lb=0, ub=2)

m.update()

for i in range(1, n-1):
    for j in range(1, n-1):
        m.addConstr(x[i, j] + x[i, j+1] + x[i, j-1] + x[i-1, j] + x[i + 1, j] == 1 + 2*y[i, j])

for i in range(n):
    m.addConstr(x[0, i] + x[i, 0] + x[n-1, i] + x[i, n-1] == 0)


'''for j in range(1, n-1):
    m.addConstr(x[0, j] + x[0, j+1] + x[1, j] + x[0, j-1] == 1 + 2*y[0, j])
    m.addConstr(x[n-1, j] + x[n-1, j+1] + x[n-2, j] + x[n-1, j-1] == 1 + 2*y[n-1, j])
    m.addConstr(x[j, 0] + x[j+1, 0] + x[j, 1] + x[j-1, 0] == 1 + 2*y[j, 0])
    m.addConstr(x[j, n-1] + x[j+1, n-1] + x[j, n-2] + x[j-1, n-1] == 1 + 2*y[j, n-1])

m.addConstr(x[0, 0] + x[1, 0] + x[0, 1] == 1 + 2*y[0, 0])
m.addConstr(x[n-1, n-1] + x[n-2, n-1] + x[n-1, n-2] == 1 + 2*y[n-1, n-1])
m.addConstr(x[0, n-1] + x[0, n-2] + x[n-2, n-1] == 1 + 2*y[0, n-1])
m.addConstr(x[n-1, 0] + x[n-2, 0] + x[n-1, n-2] == 1 + 2*y[n-1, 0])'''

m.optimize()

plt.imshow([[x[i, j].x for j in range(1, n-1)] for i in range(1, n-1)], interpolation='nearest')
plt.show()
