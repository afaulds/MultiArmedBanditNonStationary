from History import History
from machine import MachineManager
import numpy as np
from policy import PolicyManager
import sys
from utils import Cache, Timer


def evaluate(machine_type, func, formula=None):
    if formula is None:
        score_mean, score_var = __evaluate_cache(machine_type, func)
    else:
        score_mean, score_var = Cache.process(formula+":"+machine_type, __evaluate_cache, machine_type, func)
    return score_mean + score_var


def __evaluate_cache(machine_type, func):
    num_runs = 10
    scores = []
    for i in range(num_runs):
        score = __single_evaluate(machine_type, func, 5000)
        scores.append(score)
    return np.mean(scores), np.var(scores)


def __single_evaluate(machine_type, func, T):
    pm = PolicyManager()
    mm = MachineManager()
    mm.use(machine_type)
    h = History()

    # Deteremine dynamic oracle.
    for t in range(1, T):
        arm_id, prob = mm.oracle(t)
        h.store_oracle(t, arm_id, prob)

    h.reset()
    pm.use("GeneticAlgorithmPolicy", mm.get_num_arms())
    pm.set_params({"func": func})

    # Loop getting arm, playing machine, saving reward
    for t in range(1, T):
        arm_id = pm.get_arm(t)
        reward = mm.play(t, arm_id)
        pm.store(t, arm_id, reward)
        h.store(t, arm_id, reward)

    # Print results of run
    return h.get_normalized_arm_regret()
