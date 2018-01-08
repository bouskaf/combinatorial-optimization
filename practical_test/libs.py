import decimal
import numpy as np


# capacity: adjacency matrix with upper bounds
# neighbors:
# flow: initial flow, put [] in no initial flow
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

def GetNeighbors(capacity):
    neighbors = {}  # neighbors include reverse direction neighbors
    for vertex in xrange(len(capacity)):
        neighbors[vertex] = []
    for vertex, flows in enumerate(capacity):
        for neighbor, flow in enumerate(flows):
            if flow > 0:
                neighbors[vertex].append(neighbor)
                neighbors[neighbor].append(vertex)  # reverse path may be used
    return neighbors

def TransformLowerBounds(capacity, lower_bounds):
    capacity = np.asarray(capacity)
    lower_bounds = np.asarray(lower_bounds)
    size = capacity.shape[0]
    balances =  np.zeros(size, dtype=np.int)

    # 1) add edge from node t to s with infinite upper bound
    capacity[size - 1,0] = 99999
    # 2) for each edge, calculate new upper bound
    new_capacity = np.subtract(capacity, lower_bounds)
    # 3) for each vertex calculate balance
    for i in range(0, size):
        incoming_edges = 0
        outcoming_edges = 0
        for j in range(0, size):
            incoming_edges += lower_bounds[j,i]
        for j in range(0, size):
            outcoming_edges += lower_bounds[i,j]
        balances[i] = incoming_edges - outcoming_edges

    new_new_capacity = new_capacity
    new_new_capacity = np.insert(new_new_capacity, size, 0, axis=1)
    new_new_capacity = np.insert(new_new_capacity, 0, 0, axis=1)
    new_new_capacity = np.insert(new_new_capacity, size, 0, axis=0)
    new_new_capacity = np.insert(new_new_capacity, 0, 0, axis=0)

    for i in range(0, size):
        if balances[i] > 0:
            new_new_capacity[0, i+1] = balances[i]
        if balances[i] < 0:
            new_new_capacity[i+1, size + 1] = balances[i]*(-1)

    return new_new_capacity.tolist()