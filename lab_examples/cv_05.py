import gurobipy as g

__author__ = 'tonda'

file_object = open("czech_republic.txt", "r")

s = 0
t = 4

G = {(s, 1): -3, (s, 2): -6, (3, 1): -1, (2, 3): -4, (3, 5): 2, (2, 5): 1, (1, t): 2, (1, 2): -3}


m = g.Model()

x = {}
for i in range(6):
    for j in range(6):
        if (i, j) in G.keys():
            x[i, j] = m.addVar(vtype=g.GRB.BINARY, obj=G[i, j])
        else:
            x[i, j] = m.addVar(vtype=g.GRB.BINARY, ub=0)

m.update()

m.addConstr(g.quicksum([x[s, j] for j in range(6)]) == 1)
m.addConstr(g.quicksum([x[i, s] for i in range(6)]) == 0)
m.addConstr(g.quicksum([x[i, t] for i in range(6)]) == 1)
m.addConstr(g.quicksum([x[t, j] for j in range(6)]) == 0)

for i in range(6):
    if i != s and i != t:
        m.addConstr(g.quicksum([x[i, k] for k in range(6)]) == g.quicksum([x[k, i] for k in range(6)]))
        m.addConstr(g.quicksum([x[i, k] for k in range(6)]) <= 1)

m.optimize()

print("shortest s-t distance ILP:", m.objVal)
print([(i, j, x[i, j].x) for (i, j) in G.keys() if x[i, j].x > 0.5])


# bellman-ford
l = [100000]*6
l[s] = 0
for k in range(5):
    for (v, w) in G.keys():
        if l[w] > l[v] + G[v, w]:
            l[w] = l[v] + G[v, w]

print("shortest s-t distance Bellman-Ford:", l[t])



