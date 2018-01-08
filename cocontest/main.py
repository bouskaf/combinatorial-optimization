#!/usr/bin/env python2

import decimal
import sys
import gurobipy as g
import numpy as np

def parse_input(file):
    with open(file) as f:
        temp = f.readlines()
    lines = []
    for line in temp:
        lines.append(map(int, line.split(" ")))
    return lines

if __name__ == "__main__":
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    output_file = open(output_file, 'w+')
    input_text = parse_input(input_file)

    persons_nr = input_text[0][0]
    bills_nr = input_text[0][1]
    bills = input_text[1]
    who_paid = input_text[2]


    settlement_value = sum(bills) / float(persons_nr)


    balances = np.zeros(persons_nr)
    for i in range(bills_nr):
        bill = bills[i]
        person_index = who_paid[i] - 1
        balances[person_index] -= bill

    for i in range(persons_nr):
        balances[i] += settlement_value


    m = g.Model()
    m.setParam('OutputFlag', False)

    # add variables for transaction amount
    a = {}
    T = {}

    for i in range(persons_nr):
        if balances[i] < 0:
            for j in range(persons_nr):
                if i != j:
                    if balances[j] > 0:
                        a[j + 1, i + 1] = m.addVar(vtype=g.GRB.CONTINUOUS, name='a' + str(j + 1) + '_' + str(i + 1))

    for i in range(persons_nr):
        if balances[i] < 0:
            for j in range(persons_nr):
                if i != j:
                    if balances[j] > 0:
                        T[j + 1, i + 1] = m.addVar(vtype=g.GRB.BINARY, name='T' + str(j + 1) + '_' + str(i + 1))

    m.update()

    # set objective
    m.setObjective(g.quicksum(T.values()), g.GRB.MINIMIZE)

    # add constraints
    for i in range(persons_nr):
        constraint = []
        if balances[i] < 0:
            for j in range(persons_nr):
                if i != j:
                    if balances[j] > 0:
                        constraint.append(-a[j + 1, i + 1])
            if len(constraint) > 0:
                m.addConstr(g.quicksum(constraint) == balances[i])

        if balances[i] > 0:
            for j in range(persons_nr):
                if i != j:
                    if balances[j] < 0:
                        constraint.append(a[i + 1, j + 1])
            if len(constraint) > 0:
                m.addConstr(g.quicksum(constraint) == balances[i])

    for i in range(persons_nr):
        if balances[i] < 0:
            for j in range(persons_nr):
                if i != j:
                    if balances[j] >= 0:
                        m.addConstr(a[j + 1, i + 1] <= T[j + 1, i + 1] * 1000000)



    m.optimize()
    #m.write("out.lp")

    result = []

    for key, value in a.iteritems():
        temp = []
        if value.X > 0:
            temp.append(key[0])
            temp.append(key[1])
            temp.append(value.X)
            result.append(temp)

    output_file.write(str(int(round(m.objVal))) + "\n")


    for line in result:
        output_file.write(" ".join(map(str, line)) + "\n")
