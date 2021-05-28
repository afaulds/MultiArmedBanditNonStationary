from History import History
from machine import MachineManager
import json
import numpy as np
import os
from policy import PolicyManager
import matplotlib.pyplot as plt


force_policy_test = [
    "DiscountedThompsonSamplingPolicy",
]
force_machine_test = None
all_params = {}
num_runs = 10
param_range = np.linspace(0.8, 1.0, 50)


def main():
    load_param()
    pm = PolicyManager()
    mm = MachineManager()

    # Loop through all machines
    for machine_name in force_machine_test or mm.get_machine_names():

        # Initialize for machine.
        mm.use(machine_name)
        h = History()

        # Deteremine dynamic oracle.
        for t in range(1, 5000):
            arm_id, prob = mm.oracle(t)
            h.store_oracle(t, arm_id, prob)

        # Loop through all policies
        for policy_name in force_policy_test or pm.get_policy_names():
            x = [0] * len(param_range)
            y = [0] * len(param_range)
            for i in range(num_runs):
                print("Run #{}".format(i))
                for j in range(len(param_range)):
                    param_val = param_range[j]
                    h.reset()
                    pm.use(policy_name, mm.get_num_arms())
                    pm.set_params({
                       "gamma": param_val,
                    })
                    for t in range(1, 5000):
                        arm_id = pm.get_arm(t)
                        reward = mm.play(t, arm_id)
                        pm.store(t, arm_id, reward)
                        h.store(t, arm_id, reward)
                    x[j] = param_val
                    y[j] += h.get_reward() / num_runs
                    print(".", end="", flush=True)
                print("")
            plt.plot(x, y, "r^-")
            plt.title(policy_name)
            os.makedirs("results/param/", exist_ok=True)
            plt.savefig("results/param/{}_{}.png".format(mm.get_name(), policy_name))
            plt.close()


            best_param = 0
            best_reward = 0
            for i in range(len(x)):
                if y[i] > best_reward:
                    best_param = x[i]
                    best_reward = y[i]
            all_params["{}_{}".format(mm.get_name(), policy_name)] = best_param
    save_param()


def load_param():
    global all_params
    if os.path.exists("results/param/params.txt"):
        with open("results/param/params.txt", "r") as infile:
            all_params = json.loads(infile.read())

def save_param():
    with open("results/param/params.txt", "w") as outfile:
        outfile.write(json.dumps(all_params, indent=1))

if __name__ == "__main__":
    main()
