from geneticalgorithm import geneticalgorithm
import numpy as np
import os
import sys


np.seterr(all='ignore')#, invalid='ignore')
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
}
cache = {}


def main():
    ga_param = {
        'max_num_iteration': 1000,
        'population_size':10000,
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
        algorithm_parameters=ga_param
    )
    output_dict = model.run()
    solution = model.output_dict["variable"]


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
        num = -int(os.popen("python mab_ga.py '{}'".format(formula)).read())
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

    # Binary operators
    elif encoded_str[pos] in ['+', '-', '*', '/']:
        eq1_str, next_pos = convert_recursive(encoded_str, pos+1)
        eq2_str, next_pos = convert_recursive(encoded_str, next_pos)
        return ('{}{}{}'.format(eq1_str, encoded_str[pos], eq2_str), next_pos)


if __name__ == "__main__":
    main()
