from History import History
from machine import MachineManager
from policy import PolicyManager
import sys
from utils import Timer


def main():
    if len(sys.argv) <= 1:
        print("Supply formula for first argument. (i.e. 'x-a')")
        return
    formula = sys.argv[1].strip("\'")
    if len(sys.argv) == 3 and sys.argv[2] == "--show":
        show_scores = True
    else:
        show_scores = False
    score = 0
    score += evaluate(formula, "StaticMachine", T=50) / 3.0
    score += evaluate(formula, "StaticMachine", T=500) / 3.0
    score += evaluate(formula, "StaticMachine", T=5000) / 3.0
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
    return h.get_normalized_arm_regret()


if __name__ == "__main__":
    main()