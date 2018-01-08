import  numpy as np

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


#edges = [(0, 1), (1, 2), (2, 6), (6, 0), (3, 4), (5, 3), (4, 5), (7,9), (10,11), (9, 12), (12, 13), (13, 10), (11, 7)]
#print find_shortest_tour(edges)

A = [[1, 2, 3, 4],
     [2, 3, 5, 8]]

B = [[3, 7, 1, 1],
     [9, 2, 5, 2]]

#A = A[1][0:2]
#B = B[1][0:2]


A = np.asarray(A)
row_len = len(A[0])
A = A[:, row_len-3: row_len]
B = np.asarray(B)
B = B[:, 0:3]

print np.sum(np.absolute(A - B))
