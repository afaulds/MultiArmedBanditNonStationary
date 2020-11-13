import random
from History import History
import machine
import policy
from utils import Timer


def main():
    for policy_class in ["RandomPolicy", "GreedyPolicy", "OraclePolicy", "ThompsonSamplingPolicy"]:
        for machine_class in ["TestMachine", "SlowVaryingMachine", "FastVaryingMachine", "AbruptVaryingMachine", "StaticMachine"]:
            Timer.start(policy_class)
            History.init()
            machine_obj = eval("machine.{}()".format(machine_class))
            policy_obj = eval("policy.{}(machine_obj)".format(policy_class))
            for t in range(5000):
                arm_id = policy_obj.get_arm(t)
                reward = machine_obj.play(t, arm_id)
                History.store(t, arm_id, reward)
            History.print(machine_class, policy_class)
            Timer.stop(policy_class)




def greedy_with_memory_policy(t):
    epsilon = 0.05
    if random.random() < epsilon:
        return Machine.get_random()
    else:
        if t % 300 == 0:
            History.forget()
        best_percent = 0
        best_arm = 0
        for arm_id in range(7):
            percent = History.get_win_percent(arm_id)
            if percent > best_percent:
                best_percent = percent
                best_arm = arm_id
        return best_arm


def greedy_fade_policy(t):
    epsilon = 0.05
    if random.random() < epsilon:
        return Machine.get_random()
    else:
        best_percent = 0
        best_arm = 0
        for arm_id in range(7):
            percent = History.get_fade_win_percent(arm_id)
            if percent > best_percent:
                best_percent = percent
                best_arm = arm_id
        return best_arm


if __name__ == "__main__":
    main()
