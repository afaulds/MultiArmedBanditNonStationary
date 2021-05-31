from History import History
from machine import MachineManager
from policy import PolicyManager
import policy
import sys
from utils import Timer


force_policy_test = None
force_machine_test = None
T = 5000 # Max time


def main():
    Timer.start("main")
    pm = PolicyManager()
    mm = MachineManager()
    mm.use("SlowVaryingMachine")
    h = History()

    # Deteremine dynamic oracle.
    for t in range(1, T):
        arm_id, prob = mm.oracle(t)
        h.store_oracle(t, arm_id, prob)

    h.reset()
    pm.use("GeneticAlgorithmPolicy", mm.get_num_arms())
    formula = sys.argv[1].strip("\'")
    pm.set_params(formula)

    # Loop getting arm, playing machine, saving reward
    for t in range(1, T):
        arm_id = pm.get_arm(t)
        reward = mm.play(t, arm_id)
        pm.store(t, arm_id, reward)
        h.store(t, arm_id, reward)

    # Print results of run
    Timer.stop("main")
    print("{} => {}".format(formula, h.get_reward()))
    exit(h.get_reward())


if __name__ == "__main__":
    main()
