from History import History
from machine import MachineManager
import numpy as np
from policy import PolicyManager
import sys
from utils import Timer


def evaluate(func):
    num_runs = 20
    scores = []
    for i in range(num_runs):
        score = single_evaluate(func, "StaticMachine", 1000)
        scores.append(score)
    return np.mean(scores)
    return np.mean(scores) + np.var(scores)


def single_evaluate(func, policy_name, T):
    pm = PolicyManager()
    mm = MachineManager()
    mm.use(policy_name)
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
