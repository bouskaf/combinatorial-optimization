#!/usr/bin/env python2

import decimal
import sys
import numpy as np
import heapq as hq

def parse_input(file):
    with open(file) as f:
        temp = f.readlines()
    lines = []
    for line in temp:
        lines.append(map(int, line.split(" ")))
    return lines


def check_result(results, balances):
    new_balances = np.zeros((len(balances)))
    for line in results:
        pay = line[0]-1
        receive = line[1]-1
        amount = line[2]
        new_balances[pay] += amount
        new_balances[receive] -= amount

    return sum(np.add(new_balances, balances))


if __name__ == "__main__":

    debug = 0

    if len(sys.argv) > 2:

        if debug == 1:
            input_file = 'ranking/public-3.txt'
        else:
            input_file = sys.argv[1]
        output_file = sys.argv[2]
        time_limit = sys.argv[3]

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
        balances[person_index] += bill

    for i in range(persons_nr):
        balances[i] -= settlement_value


    sorded_balances = sorted(balances)
    indices = np.argsort(balances)

    for i in range(len(sorded_balances)):
        if sorded_balances[i] > 0:
            edge = i
            break

    results = []

    for i in range(edge):
        for j in range(len(sorded_balances)-1, edge-1, -1):
                if sorded_balances[i] != 0 and sorded_balances[j] != 0:
                    if sorded_balances[i] + sorded_balances[j] == 0:
                        results.append([indices[i] + 1, indices[j] + 1, -sorded_balances[i]])
                        balances[indices[i]] = 0
                        balances[indices[j]] = 0
                        sorded_balances[i] = 0
                        sorded_balances[j] = 0
                        break

    will_pay = []
    will_receive = []
    for i in range(persons_nr):
        if balances[i] < 0:
            hq.heappush(will_pay, (balances[i], i))
        if balances[i] > 0:
            hq.heappush(will_receive, (-balances[i], i))

    allowed_error = 1e-05

    cnt = 0

    while len(will_pay) != 0:
        temp_pay = hq.heappop(will_pay)
        pay_amount = -temp_pay[0]
        pay_idx = temp_pay[1]
        temp_receive = hq.heappop(will_receive)
        receive_amount = -temp_receive[0]
        receive_idx = temp_receive[1]

        if pay_amount > receive_amount:
            aaa_new_pay = pay_amount - receive_amount
            if abs(pay_amount - receive_amount) > allowed_error:
                hq.heappush(will_pay, (-aaa_new_pay, pay_idx))
            results.append([pay_idx+1, receive_idx+1, receive_amount])
        elif pay_amount < receive_amount:
            aaa_new_receive = receive_amount - pay_amount
            if abs(receive_amount - pay_amount) > allowed_error:
                hq.heappush(will_receive, (-aaa_new_receive, receive_idx))
            results.append([pay_idx+1, receive_idx+1, pay_amount])
        else:
            results.append([pay_idx+1, receive_idx+1, pay_amount])

    output_file.write(str(len(results)) + "\n")
    for line in results:
       output_file.write(" ".join(map(str, line)) + "\n")

    if debug == 1:
        print check_result(results, old_balances)