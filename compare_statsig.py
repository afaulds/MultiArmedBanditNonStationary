import os
from scipy import stats
import numpy as np

machine_type = "Static"
policy_type1 = "GeneticAlgorithm"
policy_type2 = "TS"
machine_list = []
policy_list = []
reward = {}


def main():
    read_files()
    analyze()

 
def analyze():
    a_key = "{}_{}".format(machine_type, policy_type1)
    b_key = "{}_{}".format(machine_type, policy_type2)
    a = reward[a_key]
    b = reward[b_key]
    print("{} - {}".format(a_key, np.mean(a)))
    print("{} - {}".format(b_key, np.mean(b)))
    print(stats.ttest_ind(a, b, equal_var = False))


def read_files():
    for j in range(10):
        with open("results/results{}.md".format(j), "r") as infile:
            line_num = 0
            for line in infile:
                if line_num == 0:
                    items = line.strip("\n\t").split("\t")
                    machine_list.extend(items)
                else:
                    items = line.strip("\n").split("\t")
                    p = items[0]
                    policy_list.append(p)
                    for i in range(len(items)-1):
                        m = machine_list[i]
                        key = "{}_{}".format(m, p)
                        if key not in reward:
                            reward[key] = []
                        reward[key].append(float(items[i+1]))
                line_num += 1


if __name__ == "__main__":
    main()