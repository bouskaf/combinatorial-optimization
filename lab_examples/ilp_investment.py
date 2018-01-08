import gurobipy as g

__author__ = 'jenda'

model = g.Model()
building_prices = [5,  7,  4, 3,  4,  6]
building_income = [16, 22, 12, 8, 11, 19]
investment_budget = 14

x = [model.addVar(vtype=g.GRB.BINARY) for i in building_prices]
model.update()
model.setObjective(g.quicksum([x_i*build_inc_i for x_i, build_inc_i in zip(x, building_income)]), sense=g.GRB.MAXIMIZE)


model.addConstr(g.quicksum([x_i*build_pric_i for x_i, build_pric_i in zip(x, building_prices)]) <= investment_budget)
"""""
model.addConstr(x[4] + x[5] <= 1)
model.addConstr(x[0] + x[5] <= 1)
model.addConstr(x[1] + x[2] <= 1)
"""
model.optimize()

model.write("out1.lp")

if model.Status == g.GRB.OPTIMAL:
    print([v.x for v in x])
    print(model.objVal)
else:
    print("No feasible solution found")