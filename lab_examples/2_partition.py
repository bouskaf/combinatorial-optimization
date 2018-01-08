import gurobipy as g

__author__ = 'jenda'

model = g.Model()
p = [100, 50, 50, 50, 20, 20, 10, 10]

x = [model.addVar(vtype=g.GRB.CONTINUOUS, lb=0, ub=1) for i in p]
model.update()

model.setObjective(0, sense=g.GRB.MINIMIZE)
model.addConstr(g.quicksum([x_i*p_i for x_i, p_i in zip(x, p)]) == 0.5 * sum(p))
model.optimize()

if model.Status == g.GRB.OPTIMAL:
    print([v.x for v in x])
    print(model.objVal)
else:
    print("No feasible solution found")