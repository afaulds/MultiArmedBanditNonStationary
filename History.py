import matplotlib.pyplot as plt
import numpy as np
import os


class History:

    figure = {}

    def __init__(self):
        self.oracle = {
            "time": [],
            "reward(time)": [],
            "reward_normalized(time)": [],
            "reward_total(time)": [],
            "arm(time)": [],
            "total_reward": 0,
            "plays": 0,
            "arms": [],
        }
        self.reset()

    def reset(self):
        self.stats = {
            "time": [],
            "reward(time)": [],
            "reward_normalized(time)": [],
            "reward_total(time)": [],
            "arm(time)": [],
            "total_reward": 0,
            "plays": 0,
            "arms": [],
        }

    def store_oracle(self, t, machine_id, reward):
        self.oracle["total_reward"] += reward
        self.oracle["plays"] += 1
        self.oracle["time"].append(t)
        self.oracle["reward(time)"].append(reward)
        self.oracle["reward_normalized(time)"].append(self.oracle["total_reward"] / t)
        self.oracle["reward_total(time)"].append(self.oracle["total_reward"])
        self.oracle["arm(time)"].append(machine_id)
        while machine_id >= len(self.oracle["arms"]):
            self.oracle["arms"].append({
                "rewards": 0,
                "rewards_fade": 0,
                "plays": 0,
                "daily": [],
            })
        self.oracle["arms"][machine_id]["rewards"] += reward
        self.oracle["arms"][machine_id]["plays"] += 1
        self.oracle["arms"][machine_id]["daily"].append(reward)

    def store(self, t, machine_id, reward):
        self.stats["total_reward"] += reward
        self.stats["plays"] += 1
        self.stats["time"].append(t)
        self.stats["reward(time)"].append(reward)
        self.stats["reward_normalized(time)"].append(self.stats["total_reward"] / t)
        self.stats["reward_total(time)"].append(self.stats["total_reward"])
        self.stats["arm(time)"].append(machine_id)
        while machine_id >= len(self.stats["arms"]):
            self.stats["arms"].append({
                "rewards": 0,
                "rewards_fade": 0,
                "plays": 0,
                "daily": [],
            })
        self.stats["arms"][machine_id]["rewards"] += reward
        self.stats["arms"][machine_id]["plays"] += 1
        self.stats["arms"][machine_id]["daily"].append(reward)

    def get_regret(self):
        y = (np.array(self.oracle["reward_total(time)"]) - np.array(self.stats["reward_total(time)"])) / np.array(self.stats["time"])
        return y[-1]

    def print(self, machine, policy):
        self.__print_stats(machine, policy)
        self.__plot_oracle(machine, policy)
        self.__plot_reward(machine, policy)
        self.__plot_regret(machine, policy)
        self.__plot_arm(machine, policy)

    def __print_stats(self, machine, policy):
        print("{}".format(policy))
        print("  {}".format(machine))
        print("   plays: {}".format(self.stats["plays"]))
        print("   rewards: {}".format(self.stats["total_reward"]))
        print("   percent: {}".format(1.0 * self.stats["total_reward"] / self.stats["plays"]))

    def __plot_oracle(self, machine, policy):
        x = self.oracle["time"]
        y = self.oracle["reward(time)"]
        key = "{}_oracle".format(machine)
        plt.figure(self.__get_figure_num(key))
        plt.plot(x, y)
        plt.xlim(0, 1000)
        plt.ylim(0, 1)
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/oracle.png".format(machine))
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
        y = (np.array(self.oracle["reward_total(time)"]) - np.array(self.stats["reward_total(time)"])) / np.array(self.stats["time"])
        key = "{}_regret".format(machine)
        plt.figure(self.__get_figure_num(key))
        plt.plot(x, y, label=policy)
        plt.legend()
        os.makedirs("results/{}".format(machine), exist_ok=True)
        plt.savefig("results/{}/regret.png".format(machine))

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