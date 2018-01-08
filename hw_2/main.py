#!/usr/bin/env python2

import decimal
import sys

def EdmondsKarp(capacity, neighbors, start, end, flows):
  flow = 0
  length = len(capacity)
  if len(flows) == 0:
    flows = [[0 for i in range(length)] for j in range(length)]
  while True:
    max, parent = BreadthFirstSearch(capacity, neighbors, flows, start, end)
    if max == 0:
      break
    flow = flow + max
    v = end
    while v != start:
      u = parent[v]
      flows[u][v] = flows[u][v] + max
      flows[v][u] = flows[v][u] - max
      v = u
  return (flow, flows)


def BreadthFirstSearch(capacity, neighbors, flows, start, end):
  length = len(capacity)
  parents = [-1 for i in xrange(length)] # parent table
  parents[start] = -2 # make sure source is not rediscovered
  M = [0 for i in xrange(length)] # Capacity of path to vertex i
  M[start] = decimal.Decimal('Infinity') # this is necessary!

  queue = []
  queue.append(start)
  while queue:
    u = queue.pop(0)
    for v in neighbors[u]:
      # if there is available capacity and v is is not seen before in search
      if capacity[u][v] - flows[u][v] > 0 and parents[v] == -1:
        parents[v] = u
        # it will work because at the beginning M[u] is Infinity
        M[v] = min(M[u], capacity[u][v] - flows[u][v]) # try to get smallest
        if v != end:
          queue.append(v)
        else:
          return M[end], parents
  return 0, parents


def ParseInputFile(file):
    capacity = []
    neighbors = {} # neighbors include reverse direction neighbors

    with open(file) as f:
        temp = f.readlines()

    lines = []
    for line in temp:
        lines.append(map(int, line.split(" ")))

    cust_nr = lines[0][0]
    prod_nr = lines[0][1]
    node_number = cust_nr + prod_nr + 4

    #first line
    capacity_line = [0 for i in range(0, 2)]
    for i in range(1, cust_nr + 1):
        capacity_line.append(lines[i][0])
    for i in range(prod_nr):
        capacity_line.append(0)
    demand_sum = 0
    for i in range(prod_nr):
        demand_sum += lines[-1][i]
    capacity_line.append(demand_sum)
    capacity_line.append(0)
    capacity.append(capacity_line)

    #second line
    capacity_line = [0 for i in range(0, 2)]
    lb_sum = 0
    for i in range(1, cust_nr + 1):
        lb_sum += lines[i][0]
        capacity_line.append(lines[i][1] - lines[i][0])
    for i in range(prod_nr + 1):
        capacity_line.append(0)
    capacity_line.append(lb_sum)
    capacity.append(capacity_line)

    #customers
    for i in range(1, cust_nr + 1):
        capacity_line = [0 for k in range(0, 2 + cust_nr + prod_nr + 2)]
        for j in range(2, len(lines[i])):
            capacity_line[2 + cust_nr + lines[i][j] - 1] = 1
        capacity.append(capacity_line)

    #products
    for i in range(prod_nr):
        capacity_line = [0 for k in range(0, 2 + cust_nr + prod_nr + 2)]
        capacity_line[-1] = lines[-1][i]
        capacity_line[-2] = 99999
        capacity.append(capacity_line)

    capacity_line = [0 for k in range(0, 2 + cust_nr + prod_nr + 2)]
    capacity_line[1] = 99999
    capacity.append(capacity_line)
    capacity_line = [0 for k in range(0, 2 + cust_nr + prod_nr + 2)]
    capacity.append(capacity_line)


    for vertex in xrange(len(capacity)):
        neighbors[vertex] = []
    for vertex, flows in enumerate(capacity):
        for neighbor, flow in enumerate(flows):
            if flow > 0:
                neighbors[vertex].append(neighbor)
                neighbors[neighbor].append(vertex) # reverse path may be used
    return capacity, neighbors, cust_nr, prod_nr, node_number


if __name__ == "__main__":
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    capacity, neighbors, cust_nr, prod_nr, node_number = ParseInputFile(input_file)
    flow, flows = EdmondsKarp(capacity, neighbors, 0, node_number - 1, [])

    output_file = open(output_file, 'w+')
    if flows[0] != capacity[0]:
        output_file.write('-1\n')
    else:
        flow, flows = EdmondsKarp(capacity, neighbors, 1, node_number - 2, flows)
        for k in range(2, cust_nr + 2):
            temp = []
            for i, j in enumerate(flows[k]):
                if j == 1:
                    temp.append(i-(2+cust_nr-1))
            output_file.write(' '.join(map(str, temp)) + "\n")
