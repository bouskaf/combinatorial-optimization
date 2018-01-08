#!/usr/bin/env python2

import sys
import gurobipy as g
import numpy as np

def ParseInputFile(file):
    with open(file) as f:
        temp = f.readlines()
    lines = []
    for line in temp:
        lines.append(map(int, line.rstrip().split(" ")))
    return lines


def check_cond_1(c, unused_tasks):
    for task in unused_tasks:
        if c + task[0] > task[2]:
            return False
    return True

def check_cond_2(c, unused_tasks, UB):
    if len(unused_tasks) == 0:
        return True
    min_r = 999999
    part2 = 0
    for task in unused_tasks:
        if task[1] < min_r:
            min_r = task[1]
        part2 += task[0]

    if min_r > c:
        part1 = min_r
    else:
        part1 = c

    LB = part1 + part2

    if LB > UB:
        return False
    else:
        return True

def release_time_property(solution):
   for i in range(0, len(solution)-1):
       if solution[i][1] > solution[i+1][1]:
           return False
   return True


def build_tree(unused_tasks, solution, c, UB):
    for task in unused_tasks:
        if len(solution) == task_nr:
            solution = []
        temp_unused_tasks = list(unused_tasks)
        current_task = task
        temp_unused_tasks.remove(current_task)

        old_c = c
        if current_task[1] > c:
            c = current_task[1] + current_task[0]
        else:
            c = c + current_task[0]
        if check_cond_1(c, temp_unused_tasks):
            if check_cond_2(c, temp_unused_tasks, UB):
                solution.append(current_task)
                if len(solution) == task_nr:
                    if release_time_property(solution):
                        all_solutions.append(solution)
                    return
                else:
                    build_tree(temp_unused_tasks, solution, c, UB)
        c = old_c






if __name__ == "__main__":
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        #input_file = 'instances/public_3.txt'
        output_file = sys.argv[2]

    output_file = open(output_file, 'w+')
    input_text = ParseInputFile(input_file)

    task_nr = input_text[0][0]

    tasks = []
    UB = 0
    indices = np.zeros((task_nr), dtype=np.int)

    for i in range(task_nr):
        task = input_text[i+1]
        #task.append('T'+ str(i+1))
        task.append(i + 1)
        tasks.append(task)
        if input_text[i+1][2] > UB:
            UB = input_text[i+1][2]
        indices[i] = i

    #tasks = np.asarray(tasks)
    all_solutions = []

    build_tree(tasks, [], 0, UB)


    if len(all_solutions) >= 1:
        sol = np.asarray(all_solutions)[0]

        result = np.zeros((task_nr), dtype=int)

        print sol

        cnt = 0
        for task in sol:
            task_idx = task[3]
            result[task_idx-1] = cnt
            cnt += task[0]

        for number in result:
            output_file.write(str(number) + "\n")
    else:
        output_file.write(str(-1) + "\n")




