import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import json
import os
from func_timeout import func_timeout, FunctionTimedOut


equation_size = 20
eq_parts = {
    1: "a",
    2: "b",
    3: "t",
    4: "n",
    5: "+",
    6: "-",
    7: "*",
    8: "/",
    9: "np.log(",
    10: "np.sqrt(",
    11: ")",
    12: " ",
}
cache = {}
args = None


def main():
    varbound = np.array([[1, len(eq_parts)]] * equation_size)
    model = ga(
        function=mab_run,
        dimension=equation_size,
        variable_type="int",
        variable_boundaries=varbound
    )
    output_dict = model.run()
    solution = model.output_dict["variable"]


def create_equation(eq_encoded):
    eq_str = ""
    for i in eq_encoded:
        eq_str += eq_parts[i]
    eq_str = eq_str.replace(" ", "")
    if eq_str == "":
        eq_str = "invalid"
    if eq_str.find("**") > -1:
        eq_str = "invalid"
    return eq_str


def mab_run(eq_encoded):
    global args
    args = eq_encoded
    #try:
    return func_timeout(6, mab_run_impl)
    #except e as Error:
    #    return 0


def mab_run_impl():
    global args
    eq_encoded = args

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
        num = os.system("python mab_ga.py '{}'".format(formula))
        cache[formula] = -int(num)
    return cache[formula]


if __name__ == "__main__":
    main()
