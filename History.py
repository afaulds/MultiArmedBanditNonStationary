import matplotlib.pyplot as plt
import numpy as np
import os
from utils import Settings


class History:

    figure = {}

    def __init__(self):
        self.oracle = self.__init_stats()
        self.reset()

    def reset(self):
        self.stats = self.__init_stats()

    def __init_stats(self):
        return {
            "time": [],
            "reward(time)": [],
            "reward_normalized(time)": [],
            "reward_total(time)": [],
            "arm(time)": [],
            "total_reward": 0,
            "plays": 0,
            "arms": [],
        }

    def store_oracle(self, t, arm_id, reward):
        self.oracle["total_reward"] += reward
        self.oracle["plays"] += 1
        self.oracle["time"].append(t)
        self.oracle["reward(time)"].append(reward)
        self.oracle["reward_normalized(time)"].append(self.oracle["total_reward"] / t)
        self.oracle["reward_total(time)"].append(self.oracle["total_reward"])
        self.oracle["arm(time)"].append(arm_id)

    def store(self, t, arm_id, reward):
        self.stats["total_reward"] += reward
        self.stats["plays"] += 1
        self.stats["time"].append(t)
        self.stats["reward(time)"].append(reward)
        self.stats["reward_normalized(time)"].append(self.stats["total_reward"] / t)
        self.stats["reward_total(time)"].append(self.stats["total_reward"])
        self.stats["arm(time)"].append(arm_id)

    def get_reward(self):
        return self.stats["reward_total(time)"][-1]

    def get_normalized_arm_regret(self):
        z = range(1, len(self.stats["arm(time)"]) + 1)
        y = np.divide(z - np.cumsum(np.equal(self.oracle["arm(time)"], self.stats["arm(time)"])), z)
        return y[-1]

    def print(self, machine, policy):
        self.__print_stats(machine, policy)
        self.__plot_oracle(machine, policy)
        self.__plot_reward(machine, policy)
        self.__plot_regret(machine, policy)
        self.__plot_regret_arm(machine, policy)
        self.__plot_arm(machine, policy)
        self.__write_reward(machine, policy)

    def __print_stats(self, machine, policy):
        print("{}".format(policy))
        print("  {}".format(machine))
        print("   plays: {}".format(self.stats["plays"]))
        print("   rewards: {}".format(self.stats["total_reward"]))
        print("   percent: {}".format(1.0 * self.stats["total_reward"] / self.stats["plays"]))

    def __plot_oracle(self, machine, policy):
        colors = ["b-", "g--", "r-.", "k:"]
        x = self.oracle["time"]
        key = "{}_oracle_reward".format(machine)
        plt.figure(self.__get_figure_num(key))
        y = np.array(self.oracle["reward(time)"])
        for i in range(4):
            y = np.array(self.oracle["reward(time)"])
            y[np.not_equal(self.oracle["arm(time)"], i)] = None
            plt.plot(x, y, colors[i], label="Arm {}".format(i))
        plt.legend()
        plt.xlim(0, 1000)
        plt.ylim(0, 1)
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/oracle_reward.png".format(machine))
        plt.close()
        x = self.oracle["time"]
        y = self.oracle["arm(time)"]
        key = "{}_oracle_arm".format(machine)
        plt.figure(self.__get_figure_num(key))
        plt.plot(x, y)
        plt.xlim(0, 1000)
        plt.ylim(0, 4)
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/oracle_arm.png".format(machine))
        plt.close()

    def __plot_reward(self, machine, policy):
        x = self.stats["time"]
        y = self.stats["reward_normalized(time)"]
        key = "{}_reward".format(machine)
        plt.figure(self.__get_figure_num(key))
        plt.plot(x, y, label=policy)
        plt.legend()
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/reward.png".format(machine))

    def __plot_regret(self, machine, policy):
        x = self.stats["time"]
        y = (np.array(self.oracle["reward_normalized(time)"]) - np.array(self.stats["reward_normalized(time)"]))
        key = "{}_regret".format(machine)
        plt.figure(self.__get_figure_num(key))
        plt.plot(x, y, label=policy)
        plt.legend()
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/regret.png".format(machine))

    def __plot_regret_arm(self, machine, policy):
        x = self.oracle["time"]
        z = range(1, len(x) + 1)
        y = np.divide(z - np.cumsum(np.equal(self.oracle["arm(time)"], self.stats["arm(time)"])), z)
        key = "{}_regret_arm".format(machine)
        plt.figure(self.__get_figure_num(key))
        marker = Settings.get_value("{}.marker".format(policy.split(" ")[0]), "")
        plt.plot(x, y, marker, label=policy)
        plt.legend(loc='upper left')
        ylim = Settings.get_value("{}.ylim".format(machine))
        if ylim is not None:
            plt.ylim(ylim)
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/regret_arm.png".format(machine))

    def __plot_arm(self, machine, policy):
        t = self.stats["time"]
        trailing_count = 30
        num_arms = np.array(self.stats["arm(time)"]).max() + 1
        a = []
        for j in range(len(t)):
            arm = 0
            count_max = 0
            for i in range(num_arms):
                j_end = min(j+trailing_count, len(self.stats["arm(time)"]))
                count = np.isclose(self.stats["arm(time)"][j:j_end], i).sum()
                if count > count_max:
                    count_max = count
                    arm = i
            a.append(arm)
        key = "{}_{}".format(machine, policy)
        plt.figure(self.__get_figure_num(key))
        plt.plot(t, a, label=policy)
        plt.title(policy)
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/{}_arm.png".format(machine, policy))
        plt.close()

    def __get_figure_num(self, key):
        if key not in History.figure:
            History.figure[key] = len(History.figure)
        return History.figure[key]

    def __write_reward(self, machine, policy):
        machine_list = []
        policy_list = []
        reward = {}
        if os.path.exists("results/results.md"):
            with open("results/results.md", "r") as infile:
                line_num = 0
                for line in infile:
                    if line_num == 0:
                        items = line.strip("\n\t").split("\t")
                        machine_list.extend(items)
                    else:
                        items = line.strip("\n").split("\t")
                        p = items[0]
                        policy_list.append(p)
                        for i in range(len(items)-1):
                            m = machine_list[i]
                            key = "{}_{}".format(m, p)
                            reward[key] = float(items[i+1])
                    line_num += 1
        policy = policy.split(' ')[0]
        if machine not in machine_list:
            machine_list.append(machine)
        if policy not in policy_list:
            policy_list.append(policy)
        key = "{}_{}".format(machine, policy)
        reward[key] = 1.0 * (self.stats["plays"] - self.stats["total_reward"]) / self.stats["plays"]

        with open("results/results.md", "w") as outfile:
            for machine in machine_list:
                outfile.write("\t{}".format(machine))
            outfile.write("\n")

            for policy in policy_list:
                outfile.write("{}".format(policy))
                for machine in machine_list:
                    key = "{}_{}".format(machine, policy)
                    val = 0
                    if key in reward:
                        val = reward[key]
                    outfile.write("\t{:.3f}".format(val))
                outfile.write("\n")

