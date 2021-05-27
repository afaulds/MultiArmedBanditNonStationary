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

    def store_oracle(self, t, arm_id, reward):
        self.oracle["total_reward"] += reward
        self.oracle["plays"] += 1
        self.oracle["time"].append(t)
        self.oracle["reward(time)"].append(reward)
        self.oracle["reward_normalized(time)"].append(self.oracle["total_reward"] / t)
        self.oracle["reward_total(time)"].append(self.oracle["total_reward"])
        self.oracle["arm(time)"].append(arm_id)
        while arm_id >= len(self.oracle["arms"]):
            self.oracle["arms"].append({
                "rewards": 0,
                "rewards_fade": 0,
                "plays": 0,
                "daily": [],
            })
        self.oracle["arms"][arm_id]["rewards"] += reward
        self.oracle["arms"][arm_id]["plays"] += 1
        self.oracle["arms"][arm_id]["daily"].append(reward)

    def store(self, t, arm_id, reward):
        self.stats["total_reward"] += reward
        self.stats["plays"] += 1
        self.stats["time"].append(t)
        self.stats["reward(time)"].append(reward)
        self.stats["reward_normalized(time)"].append(self.stats["total_reward"] / t)
        self.stats["reward_total(time)"].append(self.stats["total_reward"])
        self.stats["arm(time)"].append(arm_id)
        while arm_id >= len(self.stats["arms"]):
            self.stats["arms"].append({
                "rewards": 0,
                "rewards_fade": 0,
                "plays": 0,
                "daily": [],
            })
        self.stats["arms"][arm_id]["rewards"] += reward
        self.stats["arms"][arm_id]["plays"] += 1
        self.stats["arms"][arm_id]["daily"].append(reward)

    def get_regret(self):
        y = (np.array(self.oracle["reward_total(time)"]) - np.array(self.stats["reward_total(time)"])) / np.array(self.stats["time"])
        return y[-1]

    def get_reward(self):
        return self.stats["reward_total(time)"][-1]

    def print(self, machine, policy):
        self.__print_stats(machine, policy)
        self.__plot_oracle(machine, policy)
        self.__plot_reward(machine, policy)
        self.__plot_regret(machine, policy)
        self.__plot_arm(machine, policy)
        self.__write_reward(machine, policy)

    def __print_stats(self, machine, policy):
        print("{}".format(policy))
        print("  {}".format(machine))
        print("   plays: {}".format(self.stats["plays"]))
        print("   rewards: {}".format(self.stats["total_reward"]))
        print("   percent: {}".format(1.0 * self.stats["total_reward"] / self.stats["plays"]))

    def __plot_oracle(self, machine, policy):
        x = self.oracle["time"]
        y = self.oracle["reward(time)"]
        key = "{}_oracle_reward".format(machine)
        plt.figure(self.__get_figure_num(key))
        plt.plot(x, y)
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

    def __write_reward(self, machine, policy):
        machine_list = []
        policy_list = []
        reward = {}
        with open("results/results.md", "r") as infile:
            line_num = 0
            for line in infile:
                if line_num == 0:
                    items = line.strip("\n|").split("|")
                    machine_list.extend(items)
                elif line_num > 1:
                    items = line.strip("\n|").split("|")
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
        reward[key] = self.stats["total_reward"]

        with open("results/results.md", "w") as outfile:
            outfile.write("||")
            for machine in machine_list:
                outfile.write("{}|".format(machine))
            outfile.write("\n")

            outfile.write("|---|")
            for machine in machine_list:
                outfile.write("---|".format(machine))
            outfile.write("\n")

            for policy in policy_list:
                outfile.write("|{}|".format(policy))
                for machine in machine_list:
                    key = "{}_{}".format(machine, policy)
                    val = 0
                    if key in reward:
                        val = reward[key]
                    outfile.write("{:.2f}|".format(val))
                outfile.write("\n")

