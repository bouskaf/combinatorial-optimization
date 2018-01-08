#!/usr/bin/env python2

import decimal
import sys
import gurobipy as g
import numpy as np


def find_one_tour(edges):
    tour = []
    tour.append(edges[0])
    start = edges[0][0]
    temp = edges[0][1]
    edges.remove(tour[0])

    while True:
        for edge in edges:
            if edge[0] == temp:
                tour.append(edge)
                if edge[1] != start:
                    temp = edge[1]
                    edges.remove(edge)
                    break
                else:
                    edges.remove(edge)
                    return tour, edges


def find_shortest_tour(edges):
    shortest_tour = []
    while len(edges) > 1:
        tour, edges = find_one_tour(edges)
        if len(shortest_tour) == 0:
            shortest_tour = tour
        else:
            if len(tour) < len(shortest_tour):
                shortest_tour = tour
    return shortest_tour

def ParseInputFile(file):
    with open(file) as f:
        temp = f.readlines()
    lines = []
    for line in temp:
        lines.append(map(int, line.split(" ")))
    return lines

def compute_distance(A, B):
    height = A.shape[0]
    width = A.shape[1]
    A = np.asarray(A)
    B = np.asarray(B)
    A = A[:, width - 3: width]
    B = B[:, 0:3]
    return np.sum(np.absolute(A - B))

def subtourelim(model, where):
  if where == g.GRB.callback.MIPSOL:
    selected = []
    # make a list of edges selected in the solution
    for i in range(n+1):
      sol = model.cbGetSolution([model._vars[i,j] for j in range(n+1)])
      selected += [(i,j) for j in range(n+1) if sol[j] > 0.5]
    # find the shortest cycle in the selected edge list
    tour = find_shortest_tour(selected)
    if len(tour) < n:
      # add a subtour elimination constraint
      expr = 0
      for i in range(len(tour)):
          expr += model._vars[tour[i][0], tour[i][1]]
      model.cbLazy(expr <= len(tour)-1)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        #input_file = 'input_file_sheep'
        output_file = sys.argv[2]

    output_file = open(output_file, 'w+')
    input_text = ParseInputFile(input_file)

    n = input_text[0][0]
    width = input_text[0][1]
    height = input_text[0][2]

    stripes = []
    stripe = []
    for i in range(0, n):
        stripe = np.asarray(input_text[i + 1])
        stripe = np.resize(stripe, (height, 3*width))
        stripes.append(stripe)

    stripes = np.asarray(stripes)



    vars = {}

    for i in range(n):
        for j in range(n):
            if i != j:
                dist = compute_distance(stripes[i], stripes[j])
                vars[i, j] = m.addVar(obj=dist, vtype=g.GRB.BINARY, name='e' + str(i) + '_' + str(j))
            else:
                vars[i, j] = m.addVar(obj=0, ub=0, vtype=g.GRB.BINARY, name='e' + str(i) + '_' + str(j))
        m.update()

    for k in range(n):
        vars[n, k] = m.addVar(obj=0, vtype=g.GRB.BINARY, name='e' + str(n) + '_' + str(k))

    for k in range(n):
        vars[k, n] = m.addVar(obj=0, vtype=g.GRB.BINARY, name='e' + str(k) + '_' + str(n))

    vars[n, n] = m.addVar(obj=0, ub=0, vtype=g.GRB.BINARY, name='e' + str(n) + '_' + str(n))
    m.update()


    for j in range(n + 1):
        m.addConstr(g.quicksum(vars[i, j] for i in range(n + 1)) == 1)

    for i in range(n + 1):
        m.addConstr(g.quicksum(vars[i, j] for j in range(n + 1)) == 1)

    m._vars = vars
    m.params.LazyConstraints = 1
    m.optimize(subtourelim)
   # m.write("out.lp")

    final_tour = []
    for key, value in vars.iteritems():
        if value.X == 1:
            final_tour.append(key)

    final_tour = find_shortest_tour(final_tour)
    result = []

    for i in range(n+1):
        if final_tour[i][0] == n:
            dummy_index = i
        result.append(final_tour[i][0])
    part1 = result[dummy_index+1: len(final_tour)]
    part2 = result[0:dummy_index]
    result = np.concatenate((part1, part2), axis=0)
    output_file.write(" ".join(map(str, result.astype(int))))


