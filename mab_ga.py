from History import History
from machine import MachineManager
from policy import PolicyManager
import sys
from utils import Timer


def main():
    formula = sys.argv[1].strip("\'")
    score = evaluate(formula, "SlowVaryingMachine")
    if score > 3000:
        score += evaluate(formula, "FastVaryingMachine")
        score += evaluate(formula, "AbruptVaryingMachine")
    print(score)


def evaluate(formula, policy_name, T=5000):
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
    pm.set_params({"eq_str": formula})

    # Loop getting arm, playing machine, saving reward
    for t in range(1, T):
        arm_id = pm.get_arm(t)
        reward = mm.play(t, arm_id)
        pm.store(t, arm_id, reward)
        h.store(t, arm_id, reward)

    # Print results of run
    return h.get_reward()


if __name__ == "__main__":
    main()
