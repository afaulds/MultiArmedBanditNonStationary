import matplotlib.pyplot as plt
import random
from utils import Timer


stats = {}


def main():
    Timer.start("main")
    for policy in ["which0", "which1", "which2", "which3", "which4"]:
        init_stats()
        for t in range(500):
            # Determine which arm to pull
            id = eval("{}(t)".format(policy))
            # Pull Arm
            reward = play(t, id)
            store(t, id, reward)
        print_stats(policy)
    Timer.stop("main")


def init_stats():
    global stats
    stats = {
        "t": [],
        "r": [],
        "total_reward": 0,
        "plays": 0,
        "arms": [],
    }


def print_stats(policy):
    t = stats["t"]
    r = stats["r"]
    del stats["t"]
    del stats["r"]
    del stats["arms"]
    stats["reward_percent"] = 1.0 * stats["total_reward"] / stats["plays"]
    print(policy)
    print(stats)
    plt.plot(t,r)
    plt.savefig("results/{}.png".format(policy))


def which0(t):
    if t > 200:
        return 6
    else:
        return 0


def which1(t):
    return 0


def which2(t):
    return random.randrange(7)


def which3(t):
    return random.randrange(7)


def which3(t):
    return random.randrange(6)


def which4(t):
    epsilon = 0.01
    if random.random() < epsilon:
        return random.randrange(7)
    else:
        best_percent = 0
        best_arm = 0
        for arm_id in range(7):
            if arm_id < len(stats["arms"]) and stats["arms"][arm_id]["plays"] > 0:
                percent = 1.0 * stats["arms"][arm_id]["rewards"] / stats["arms"][arm_id]["plays"]
                if percent > best_percent:
                    best_percent = percent
                    best_arm = arm_id
        return arm_id


def play(t, machine_id):
    if t > 200:
        if machine_id == 0:
            return random.random() < 0.1
        elif machine_id == 1:
            return random.random() < 0.2
        elif machine_id == 2:
            return random.random() < 0.3
        elif machine_id == 3:
            return random.random() < 0.4
        elif machine_id == 4:
            return random.random() < 0.5
        elif machine_id == 5:
            return random.random() < 0.6
        elif machine_id == 6:
            return random.random() < 0.9
    else:
        if machine_id == 0:
            return random.random() < 0.9
        elif machine_id == 1:
            return random.random() < 0.6
        elif machine_id == 2:
            return random.random() < 0.5
        elif machine_id == 3:
            return random.random() < 0.4
        elif machine_id == 4:
            return random.random() < 0.3
        elif machine_id == 5:
            return random.random() < 0.2
        elif machine_id == 6:
            return random.random() < 0.1


def store(t, machine_id, reward):
    stats["total_reward"] += reward
    stats["plays"] += 1
    stats["t"].append(t)
    stats["r"].append(stats["total_reward"])
    while machine_id >= len(stats["arms"]):
        stats["arms"].append({
            "rewards": 0,
            "plays": 0,
        })
    stats["arms"][machine_id]["rewards"] += reward
    stats["arms"][machine_id]["plays"] += 1


if __name__ == "__main__":
    main()
