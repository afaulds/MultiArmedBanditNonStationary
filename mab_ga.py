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
    score = evaluate(formula, "SlowVaryingMachine")
    if show_scores:
        print("SlowVaryingMachine {}".format(score))
    if score > 3000:
        score2 = evaluate(formula, "FastVaryingMachine")
        score += score2
        if show_scores:
            print("FastVaryingMachine {}".format(score2))

        score3 = evaluate(formula, "AbruptVaryingMachine")
        score += score3
        if show_scores:
            print("AbruptVaryingMachine {}".format(score3))

        score4 = evaluate(formula, "AdversarialMachine")
        score += score4
        if show_scores:
            print("AdversarialMachine {}".format(score4))

        score5 = evaluate(formula, "StaticMachine")
        score += score5
        if show_scores:
            print("StaticMachine {}".format(score5))

        score6 = evaluate(formula, "NonCycleVaryingMachine")
        score += score6
        if show_scores:
            print("NonCycleVaryingMachine {}".format(score6))
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
