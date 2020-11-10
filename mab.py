import matplotlib.pyplot as plt
import random
from util import Timer


stats = {}


def main():
    Timer.start("main")
    for policy in ["which1", "which2", "which3"]:
        print(policy)
        init_stats()
        for t in range(5000):
            # Determine which arm to pull
            id = eval("{}()".format(policy))
            # Pull Arm
            reward = play(id)
            store(t, id, reward)
        print_stats()
    Timer.stop("main")


def init_stats():
    global stats
    stats = {
        "t": [],
        "r": [],
        "total_reward": 0,
        "plays": 0,
    }


def print_stats():
    t = stats["t"]
    r = stats["r"]
    del stats["t"]
    del stats["r"]
    stats["reward_percent"] = 1.0 * stats["total_reward"] / stats["plays"]
    print(stats)
    plt.plot(t,r)
    plt.show()


def which1():
    return 0


def which2():
    return random.randrange(7)


def which3():
    return random.randrange(7)


def play(machine_id):
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


def store(t, machine_id, reward):
    stats["total_reward"] += reward
    stats["plays"] += 1
    stats["t"].append(t)
    stats["r"].append(stats["total_reward"])


if __name__ == "__main__":
    main()
