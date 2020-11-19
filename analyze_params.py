from History import History
from machine import MachineManager
import numpy as np
from policy import PolicyManager
import matplotlib.pyplot as plt


force_policy_test = [
    #"DiscountedThompsonSamplingPolicy",
    #"DiscountedOptimisticThompsonSamplingPolicy",
    "RecurringMemoryThompsonSamplingPolicy",
]
force_machine_test = [
    "AbruptVaryingMachine",
    "FastVaryingMachine",
    "SlowVaryingMachine",
]
num_runs = 5
param_range = np.linspace(0.8,1.0,41)

def main():
    pm = PolicyManager()
    mm = MachineManager()
    for machine_name in force_machine_test or mm.get_machine_names():
        mm.use(machine_name)
        h = History()

        # Deteremine dynamic oracle.
        for t in range(1, 5000):
            arm_id = mm.oracle(t)
            reward = mm.play(t, arm_id)
            h.store_oracle(t, arm_id, reward)

        for policy_name in force_policy_test or pm.get_policy_names():
            x = [0] * len(param_range)
            y = [0] * len(param_range)
            for i in range(num_runs):
                print("Run #{}".format(i))
                for j in range(len(param_range)):
                    gamma = param_range[j]
                    h.reset()
                    pm.use(policy_name, mm.get_num_machines())
                    pm.set_params({
                       "gamma": gamma,
                    })
                    for t in range(1, 5000):
                        arm_id = pm.get_arm(t)
                        reward = mm.play(t, arm_id)
                        pm.store(t, arm_id, reward)
                        h.store(t, arm_id, reward)
                    x[j] = gamma
                    y[j] += h.get_regret() / num_runs
            plt.plot(x, y, label=mm.get_name())
            plt.title(policy_name)
            plt.savefig("results/{}_param.png".format(mm.get_name(), policy_name))
            plt.close()


if __name__ == "__main__":
    main()
