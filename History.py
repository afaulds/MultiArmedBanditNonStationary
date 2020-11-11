import matplotlib.pyplot as plt


class History:

    stats = {}

    @staticmethod
    def init():
        History.stats = {
            "t": [],
            "r": [],
            "total_reward": 0,
            "plays": 0,
            "arms": [],
        }

    @staticmethod
    def store(t, machine_id, reward):
        History.stats["total_reward"] += reward
        History.stats["plays"] += 1
        History.stats["t"].append(t)
        History.stats["r"].append(History.stats["total_reward"])
        while machine_id >= len(History.stats["arms"]):
            History.stats["arms"].append({
                "rewards": 0,
                "plays": 0,
            })
        History.stats["arms"][machine_id]["rewards"] += reward
        History.stats["arms"][machine_id]["plays"] += 1

    @staticmethod
    def print(policy):
        t = History.stats["t"]
        r = History.stats["r"]
        print(policy)
        print("  plays: {}".format(History.stats["plays"]))
        print("  rewards: {}".format(History.stats["total_reward"]))
        print("  percent: {}".format(1.0 * History.stats["total_reward"] / History.stats["plays"]))
        plt.plot(t,r,label=policy)
        plt.legend()
        plt.savefig("results/reward.png".format(policy))

    @staticmethod
    def get_win_percent(arm_id):
        if arm_id < len(History.stats["arms"]) and History.stats["arms"][arm_id]["plays"] > 0:
            return 1.0 * History.stats["arms"][arm_id]["rewards"] / History.stats["arms"][arm_id]["plays"]
        else:
            return 0.0
