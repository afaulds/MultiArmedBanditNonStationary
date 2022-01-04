from deap import algorithms
from deap import base
from deap import creator
from deap import gp
from deap import tools
import math
import multiprocessing
import numpy as np
import operator
import os
import random
from gp_shared_operators import *
from gp_eval_mab import *

if len(sys.argv) == 2:
    machine_type = sys.argv[1]
else:
    machine_type = None

pset = gp.PrimitiveSetTyped("main", [float, float, float, float], float)
pset.addPrimitive(add, [float, float], float)
pset.addPrimitive(sub, [float, float], float)
pset.addPrimitive(mul, [float, float], float)
pset.addPrimitive(protected_div, [float, float], float)
pset.addPrimitive(protected_log, [float], float)
pset.addPrimitive(protected_sqrt, [float], float)
pset.addPrimitive(neg, [float], float)
pset.addPrimitive(cos, [float], float)
pset.addPrimitive(sin, [float], float)
pset.addPrimitive(min, [float, float], float)
pset.addPrimitive(max, [float, float], float)
pset.addPrimitive(protected_beta, [float, float], float)
pset.addPrimitive(sigmoid, [float], float)
#pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
#pset.renameArguments(ARG0="eq")
pset.renameArguments(ARG0="a")
pset.renameArguments(ARG1="b")
pset.renameArguments(ARG2="n")
pset.renameArguments(ARG3="t")

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual):
    formula = str(individual)
    func = toolbox.compile(expr=individual)
    score = evaluate(machine_type, func, formula)
    return score,

toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    pop = toolbox.population(n=500)
    hof = tools.HallOfFame(10)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 100, stats=mstats,
                                   halloffame=hof, verbose=True)
    # print log
    with open("solutions.txt", "a") as outfile:
        for individual in hof:
            func = toolbox.compile(expr=individual)
            score = evaluate(machine_type, func)
            outfile.write("{}\t{}\t{}\n".format(machine_type, individual, score))

if __name__ == "__main__":
    main()
