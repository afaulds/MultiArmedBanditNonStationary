import matplotlib.pyplot as plt
import numpy as np


class History:

    stats = {}
    figure = {}

    @staticmethod
    def init():
        History.stats = {
            "time": [],
            "reward(time)": [],
            "arm(time)": [],
            "total_reward": 0,
            "plays": 0,
            "arms": [],
        }

    @staticmethod
    def forget():
        History.stats["arms"] = []

    @staticmethod
    def store(t, machine_id, reward):
        History.stats["total_reward"] += reward
        History.stats["plays"] += 1
        History.stats["time"].append(t)
        History.stats["reward(time)"].append(History.stats["total_reward"])
        History.stats["arm(time)"].append(machine_id)
        while machine_id >= len(History.stats["arms"]):
            History.stats["arms"].append({
                "rewards": 0,
                "rewards_fade": 0,
                "plays": 0,
                "daily": [],
            })
        History.stats["arms"][machine_id]["rewards"] += reward
        History.stats["arms"][machine_id]["rewards_fade"] = reward + History.stats["arms"][machine_id]["rewards_fade"] / 2.0
        History.stats["arms"][machine_id]["plays"] += 1
        History.stats["arms"][machine_id]["daily"].append(reward)

    @staticmethod
    def print(machine, policy):
        t = History.stats["time"]
        r = History.stats["reward(time)"]
        print("{}".format(machine, policy))
        print("  {}".format(machine, policy))
        print("   plays: {}".format(History.stats["plays"]))
        print("   rewards: {}".format(History.stats["total_reward"]))
        print("   percent: {}".format(1.0 * History.stats["total_reward"] / History.stats["plays"]))
        if machine not in History.figure:
            History.figure[machine] = len(History.figure)
        plt.figure(History.figure[machine])
        plt.plot(t, r, label=policy)
        plt.legend()
        plt.savefig("results/{}_reward.png".format(machine))

        trailing_count = 30
        #a_map = []
        #num_arms = np.array(History.stats["arm(time)"]).max() + 1
        #for i in range(num_arms):
        #    a_map.append([])
        #    for j in range(len(t)):
        #        j_end = min(j+trailing_count, len(History.stats["arm(time)"]))
        #        a_map[i].append(1.0 - 1.0 * np.isclose(History.stats["arm(time)"][j:j_end], i).sum() / trailing_count)
        #plt.figure(1)
        #im = plt.imshow(a_map, cmap="gray")
        #plt.plot(t,a,label=policy)
        #plt.legend()
        #plt.savefig("results/{}_arm_map.png".format(policy))
        #plt.clf()

        num_arms = np.array(History.stats["arm(time)"]).max() + 1
        a = []
        for j in range(len(t)):
            arm = 0
            count_max = 0
            for i in range(num_arms):
                j_end = min(j+trailing_count, len(History.stats["arm(time)"]))
                count = np.isclose(History.stats["arm(time)"][j:j_end], i).sum()
                if count > count_max:
                    count_max = count
                    arm = i
            a.append(arm)
        key = machine + "_" + policy
        if key not in History.figure:
            History.figure[key] = len(History.figure)
        plt.figure(History.figure[key])
        plt.plot(t, a)
        plt.savefig("results/{}_{}_arm.png".format(machine, policy))
        plt.clf()

    @staticmethod
    def get_win_percent(arm_id):
        if arm_id < len(History.stats["arms"]) and History.stats["arms"][arm_id]["plays"] > 0:
            return 1.0 * History.stats["arms"][arm_id]["rewards"] / History.stats["arms"][arm_id]["plays"]
        else:
            return 1.0

    @staticmethod
    def get_win_count(arm_id):
        if arm_id < len(History.stats["arms"]) and History.stats["arms"][arm_id]["plays"] > 0:
            return History.stats["arms"][arm_id]["rewards"]
        else:
            return 1

    @staticmethod
    def get_loss_count(arm_id):
        if arm_id < len(History.stats["arms"]) and History.stats["arms"][arm_id]["plays"] > 0:
            return History.stats["arms"][arm_id]["plays"] - History.stats["arms"][arm_id]["rewards"]
        else:
            return 1.0

    @staticmethod
    def get_fade_win_percent(arm_id):
        if arm_id < len(History.stats["arms"]) and History.stats["arms"][arm_id]["plays"] > 0:
            return 1.0 * History.stats["arms"][arm_id]["rewards_fade"] / History.stats["arms"][arm_id]["plays"]
        else:
            return 1.0
