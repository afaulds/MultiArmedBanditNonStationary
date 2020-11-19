from History import History
from machine import MachineManager
from policy import PolicyManager
import matplotlib.pyplot as plt


force_policy_test = [
    "DiscountedThompsonSamplingPolicy",
    #"DiscountedOptimisticThompsonSamplingPolicy",
    #"RecurringMemoryThompsonSamplingPolicy",
]
force_machine_test = [
    "AbruptVaryingMachine",
    "FastVaryingMachine",
    "SlowVaryingMachine",
]
num_runs = 20
resolution = 40

def main():
    pm = PolicyManager()
    mm = MachineManager()
    for machine_name in force_machine_test or mm.get_machine_names():
        for policy_name in force_policy_test or pm.get_policy_names():
            x = [0] * resolution
            y = [0] * resolution
            for i in range(num_runs):
                for j in range(0, resolution):
                    gamma = 1.0 * j / resolution
                    h = History()
                    mm.use(machine_name)
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
                    y[j] += h.get_total_rewards() / num_runs
                    print("{} - {}".format(gamma, h.get_total_rewards()))
            plt.plot(x, y, label=mm.get_name())
            plt.title(policy_name)
            plt.savefig("results/{}_param.png".format(mm.get_name(), policy_name))
            plt.close()


if __name__ == "__main__":
    main()
