import gurobipy as g

__author__ = 'jenda'

model = g.Model()
c = [[0,            8,            float('inf'), float('inf'), float('inf')],
     [8,            0,            1,            7,            float('inf')],
     [float('inf'), 1,            0,            2,            12],
     [float('inf'), 7,            2,            0,            6],
     [float('inf'), float('inf'), 12,           6,            0]]

l = [model.addVar(vtype=g.GRB.CONTINUOUS, lb=0) for i in range(len(c))]
model.update()

model.setObjective(l[4], sense=g.GRB.MAXIMIZE)
model.addConstr(l[0] == 0)
model.addConstr((l[j] <= l[i] + c[i][j] for i in range(len(c)) for j in range(len(c))))
model.optimize()

if model.Status == g.GRB.OPTIMAL:
    print([v.x for v in l])
    print(model.objVal)
else:
    print("No feasible solution found")