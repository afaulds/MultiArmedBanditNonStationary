from geneticalgorithm import geneticalgorithm
import json
import numpy as np
import os
import sys


equation_size = 40
eq_parts = {
    1: "a",
    2: "b",
    3: "t",
    4: "n",
    5: "+",
    6: "-",
    7: "*",
    8: "/",
    9: "|", # - (negative)
    10: "L", # np.log
    11: "Q", # np.sqrt
    12: "B", # np.random.beta
    13: "C", # np.cos
    14: "S", # np.sin
    15: "R", # np.random.random_sample
    16: "N", # min
    17: "M", # max
}
cache = {}


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--show":
        eval_best()
    else:
        ga_run()

def eval_best():
    solutions = get_solutions()
    for solution in solutions:
        mab_run(solution)


def ga_run():
    ga_param = {
        'max_num_iteration': 1000,
        'population_size':1000,
        'mutation_probability':0.1,
        'elit_ratio': 0.01,
        'crossover_probability': 0.5,
        'parents_portion': 0.3,
        'crossover_type':'uniform',
        'max_iteration_without_improv':None
    }
    varbound = np.array([[1, len(eq_parts)]] * equation_size)
    model = geneticalgorithm(
        function=mab_run,
        dimension=equation_size,
        variable_type="int",
        variable_boundaries=varbound,
        function_timeout=50,
        convergence_curve=False,
        algorithm_parameters=ga_param
    )
    model.set_pop(get_solutions())
    output_dict = model.run()
    solution = model.output_dict["variable"]
    add_solution(solution.tolist())


def mab_run(eq_encoded):
    # Test if valid formula.
    a = 5
    b = 2
    n = 7
    t = 3
    formula = create_equation(eq_encoded)
    try:
        eval(formula)
    except:
        return 0
    # Calculate MAB result.
    # Cache results for same formula to speed up results
    if formula not in cache:
        num = float(os.popen("python mab_ga_static.py '{}'".format(formula)).read())
        print("{} => {}".format(formula, num))
        cache[formula] = num
    return cache[formula]


def create_equation(eq_encoded):
    eq_str = ""
    for i in eq_encoded:
        eq_str += eq_parts[i]
    return convert(eq_str)


def convert(encoded_str):
    return convert_recursive(encoded_str)[0]


def convert_recursive(encoded_str, pos=0):
    # Got to end of string
    if pos >= len(encoded_str):
        return ("", pos+1)

    # Variables
    if encoded_str[pos] in ['a', 'b', 't', 'n']:
        return (encoded_str[pos], pos+1)

    if encoded_str[pos] == 'R':
        return ('np.random.random_sample()', pos+1)

    # Unary operators
    elif encoded_str[pos] == '|':
        eq_str, next_pos = convert_recursive(encoded_str, pos+1)
        return ('-{}'.format(eq_str), next_pos)
    elif encoded_str[pos] == 'L':
        eq_str, next_pos = convert_recursive(encoded_str, pos+1)
        return ('np.log({})'.format(eq_str), next_pos)
    elif encoded_str[pos] == 'Q':
        eq_str, next_pos = convert_recursive(encoded_str, pos+1)
        return ('np.sqrt({})'.format(eq_str), next_pos)
    elif encoded_str[pos] == 'C':
        eq_str, next_pos = convert_recursive(encoded_str, pos+1)
        return ('np.cos({})'.format(eq_str), next_pos)
    elif encoded_str[pos] == 'S':
        eq_str, next_pos = convert_recursive(encoded_str, pos+1)
        return ('np.sin({})'.format(eq_str), next_pos)

    # Binary operators
    elif encoded_str[pos] in ['+', '-', '*', '/']:
        eq1_str, next_pos = convert_recursive(encoded_str, pos+1)
        eq2_str, next_pos = convert_recursive(encoded_str, next_pos)
        return ('({}{}{})'.format(eq1_str, encoded_str[pos], eq2_str), next_pos)
    elif encoded_str[pos] == 'B':
        eq1_str, next_pos = convert_recursive(encoded_str, pos+1)
        eq2_str, next_pos = convert_recursive(encoded_str, next_pos)
        return ('np.random.beta({},{})'.format(eq1_str, encoded_str[pos], eq2_str), next_pos)
    elif encoded_str[pos] == 'M':
        eq1_str, next_pos = convert_recursive(encoded_str, pos+1)
        eq2_str, next_pos = convert_recursive(encoded_str, next_pos)
        return ('max({},{})'.format(eq1_str, encoded_str[pos], eq2_str), next_pos)
    elif encoded_str[pos] == 'N':
        eq1_str, next_pos = convert_recursive(encoded_str, pos+1)
        eq2_str, next_pos = convert_recursive(encoded_str, next_pos)
        return ('max({},{})'.format(eq1_str, encoded_str[pos], eq2_str), next_pos)


def get_solutions():
    if os.path.exists("solutions.json"):
        with open("solutions.json", "r") as infile:
            solutions = json.loads(infile.read())
        solutions = np.unique(solutions, axis=0).tolist()
    else:
        solutions = []
    return solutions


def add_solution(solution):
    solutions = get_solutions()
    solutions.append(solution)
    with open("solutions.json", "w") as outfile:
        outfile.write(json.dumps(solutions))

if __name__ == "__main__":
    main()
