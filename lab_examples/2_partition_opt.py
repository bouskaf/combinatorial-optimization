import gurobipy as g

__author__ = 'jenda'

model = g.Model()
#p = [100, 50, 50, 50, 20, 20, 10, 10]

p = [5, 2, 4, 2, 3, 6]
x = [model.addVar(vtype=g.GRB.INTEGER, lb=0, ub=1) for i in p]
C_max = model.addVar(vtype=g.GRB.CONTINUOUS, lb=0)
model.update()

print zip(x,p)


model.setObjective(C_max, sense=g.GRB.MINIMIZE)
model.addConstr(g.quicksum([x_i*p_i for x_i, p_i in zip(x, p)]) <= C_max)
model.addConstr(g.quicksum([(1-x_i)*p_i for x_i, p_i in zip(x, p)]) <= C_max)
model.optimize()

if model.Status == g.GRB.OPTIMAL:
    print([v.x for v in x])
    print(model.objVal)
else:
    print("No feasible solution found")