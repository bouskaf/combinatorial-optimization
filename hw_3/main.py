#!/usr/bin/env python2

import gurobipy as g
import sys
import numpy as np

def calculateProjections(P1, P2, I):
    if ((P1 == 'C') and (P2 == 'R') or (P1 == 'R') and (P2 == 'C')):
        size1 = len(sumC);
        size2 = len(sumR);
        size3 = size1 + size2;

        # matrices creation
        b = np.concatenate((sumR, -sumC), axis=0)
        l = np.zeros((size3, size3))
        u_1 = np.zeros((size1, size1))
        u_2 = np.ones((size1, size1))
        u_3 = np.zeros((size1, size3))
        c_1 = np.zeros((size1, size1))
        c_2 = np.ones((size1, size1)) - I
        c_3 = np.zeros((size1, size3))
        u = np.concatenate((u_1, u_2), axis=1)
        u = np.concatenate((u, u_3), axis=0)
        c = np.concatenate((c_1, c_2), axis=1)
        c = np.concatenate((c, c_3), axis=0)

        # flow calculation
        F = mincostflow(c, l, u, b)

        # image reconstruction
        I = F[0:size1, size2:len(F)]


    if ((P1 == 'C') and (P2 == 'D') or (P1 == 'D') and (P2 == 'C')):
        size1 = len(sumC)
        size2 = len(sumD)
        size3 = size1 + size2

        # matrices creation
        b = np.concatenate((sumC, -sumD), axis=0)
        l = np.zeros((size3, size3))
        u = np.zeros((size3, size3))
        c = np.zeros((size3, size3))
        for ii in range(0, size1):
            for j in range(size1 + ii, 2 * size1 + ii):
                u[ii, j] = 1
                c[ii, j] = 1 - I[2 * size1 - j + ii - 1, ii];

        # flow calculation
        F = mincostflow(c, l, u, b)

        # image reconstruction
        for ii in range(0, size1):
            for j in range(size1 + ii, 2 * size1 + ii):
                I[2 * size1 - j + ii - 1, ii] = F[ii, j];

    if ((P1 == 'C') and (P2 == 'A') or (P1 == 'A') and (P2 == 'C')):
        size1 = len(sumC)
        size2 = len(sumA)
        size3 = size1 + size2

        # matrices creation
        b = np.concatenate((sumC, -sumA), axis=0)
        l = np.zeros((size3, size3))
        u = np.zeros((size3, size3))
        c = np.zeros((size3, size3))
        for ii in range(0, size1):
            for j in range(size1 + ii, (2 * size1 + ii)):
                u[ii, j] = 1;
                c[ii, j] = 1 - I[j - size1 - ii, ii]

        # flow calculation
        F = mincostflow(c, l, u, b)

        # image reconstruction
        for ii in range(0, size1):
            for j in range(size1 + ii, (2 * size1 + ii)):
                I[j - size1 - ii, ii] = F[ii, j];

    if ((P1 == 'R') and (P2 == 'D') or (P1 == 'D') and (P2 == 'R')):
        size1 = len(sumR);
        size2 = len(sumD);
        size3 = size1 + size2;

        # matrices creation
        b = np.concatenate((sumR, -sumD), axis=0)
        l = np.zeros((size3, size3))
        u = np.zeros((size3, size3))
        c = np.zeros((size3, size3))

        for ii in range(0, size1):
            for j in range(2 * size1 - 1 - ii , size3 - ii):
                u[ii, j] = 1
                c[ii, j] = 1 - I[ii, j - size2 + ii];

        # flow calculation
        F = mincostflow(c, l, u, b)

        # image reconstruction
        for ii in range(0, size1):
            for j in range(2 * size1 - 1 - ii , size3 - ii):
                I[ii, j - size2 + ii] = F[ii, j];

    if ((P1 == 'R') and (P2 == 'A') or (P1 == 'A') and (P2 == 'R')):
        size1 = len(sumR)
        size2 = len(sumA)
        size3 = size1 + size2

        # matrices creation
        b = np.concatenate((sumR, -sumA), axis=0)
        l = np.zeros((size3, size3))
        u = np.zeros((size3, size3))
        c = np.zeros((size3, size3))
        for ii in range(0, size1):
            for j in range(size1 + ii, (2 * size1 + ii)):
                u[ii, j] = 1;
                c[ii, j] = 1 -  I[ii, j - size1 - ii]

        # flow calculation
        F = mincostflow(c, l, u, b)

        # image reconstruction
        for ii in range(0, size1):
            for j in range(size1 + ii , size3 - size1 + ii + 1):
                I[ii, j - size1 - ii] = F[ii, j];

    if ((P1 == 'D') and (P2 == 'A') or (P1 == 'A') and (P2 == 'D')):
        size1 = len(sumD)
        size2 = len(sumA)
        size3 = size1 + size2
        size4 = len(sumR)

        # matrices creation
        b = np.concatenate((sumD, -sumA), axis=0)
        l = np.zeros((size3, size3))
        u = np.zeros((size3, size3))
        c = np.zeros((size3, size3))
        m = 0;
        for j in range(size3 - size4, size1 - 1, -1):
            for k in range(0, size4):
                u[m + k, j + k] = 1;
                c[m + k, j + k] = 1 - I[j - size2, k]
            m += 1;

        # flow calculation
        F = mincostflow(c, l, u, b)

        # image reconstruction
        m = 0
        for j in range(size3 - size4, size1 - 1, -1):
            for k in range(0, size4):
                I[j - size2, k] = F[m + k, j + k]
            m += 1;

    return I

def mincostflow(c, l, u, b):
    el_nr = len(np.ravel(c))
    node_nr = len(c)
    model = g.Model()
    model.setParam( 'OutputFlag', False )
    f = [model.addVar(lb=0, ub=1, vtype=g.GRB.INTEGER, name='f'+str(i)) for i in range(0, el_nr)]
    model.update()
    c_resized = np.ravel(c).tolist()
    model.setObjective(g.quicksum([c_i * f_i for c_i, f_i in zip(c_resized, f)]), sense=g.GRB.MINIMIZE)

    for i in range(0, node_nr):
        outgoing = []
        for j in range(0, node_nr):
            outgoing.append(u[i][j]*f[getIndexByIndeces(i,j,node_nr)])
        incoming = []
        for j in range(0, node_nr):
            incoming.append(u[j][i]*f[getIndexByIndeces(j,i,node_nr)])
        model.addConstr(g.quicksum(outgoing) - g.quicksum(incoming) == b[i])

    model.optimize()
    model.write("out.lp")

    if model.Status == g.GRB.OPTIMAL:
        #print model.objVal
        result = [v.x for v in f]
        result = map(int, result)
        result = np.asarray(result)
        result = np.resize(result, (node_nr, node_nr))
        return result
    else:
        return 0

def getIndexByIndeces(i,j, dim):
    return i*dim + j

def ParseInputFile(file):
    with open(file) as f:
        temp = f.readlines()
    lines = []
    for i in range(0, len(temp)-1):
        lines.append(map(int, temp[i].split(" ")))
    lines.append(map(str, temp[len(temp)-1].split(" ")))
    return lines

if __name__ == "__main__":
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    output_file = open(output_file, 'w+')

    input = ParseInputFile(input_file)

    dimension = input[0][0]
    iterations = input[0][1]

    sumR = np.asarray(input[1])
    sumC = np.asarray(input[2])
    sumA = np.asarray(input[3])
    sumD = np.asarray(input[4])

    projections = input[5]

    I = np.zeros((dimension, dimension))
    for i in range(0, len(projections), 2):
        P1 = projections[i]
        P2 = projections[i+1]
        I = calculateProjections(P1, P2, I)

    for line in I:
        output_file.write(" ".join(map(str, line)))
        output_file.write("\n")