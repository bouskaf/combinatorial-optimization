import gurobipy as g

__author__ = 'tonda'


m = g.Model()

x1 = m.addVar(vtype=g.GRB.INTEGER, lb=0)
x2 = m.addVar(vtype=g.GRB.INTEGER, lb=0)

m.update()

#m.setObjective(-x1 + 2*x2, sense=g.GRB.MAXIMIZE)
m.setObjective(x1 + x2, sense=g.GRB.MAXIMIZE)

#m.addConstr(2*x1 + x2 <= 5)
#m.addConstr(-4*x1 + 4*x2 <= 5)

m.addConstr(2*x1 + x2 <= 6)
m.addConstr(-2*x1 + 2*x2 <= 3)

#m.addConstr(x1 >= 1)
#m.addConstr(x2 <= 2)


m.optimize()
print(x1.x, x2.x, m.objVal)


















#m.optimize()

#m.addConstr(x1 >= 2)
#m.optimize()
#print(x1.x, x2.x)

#m.addConstr(x1 <= 1)
#m.optimize()
#print(x1.x, x2.x)

#m.addConstr(x2 <= 2)
#m.optimize()
#print(x1.x, x2.x)

#m.addConstr(x1 <= 0)
#m.optimize()
#print(x1.x, x2.x)

#m.addConstr(x2 <= 1)
#m.optimize()
#print(x1.x, x2.x)
