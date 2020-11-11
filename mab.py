import random
from History import History
from utils import Timer


def main():
    for policy in ["perfect_policy", "random_policy", "greedy_policy"]:
        Timer.start(policy)
        History.init()
        for t in range(50000):
            # Determine which arm to pull
            id = eval("{}(t)".format(policy))
            # Pull Arm
            reward = play(t, id)
            History.store(t, id, reward)
        History.print(policy)
        Timer.stop(policy)


def perfect_policy(t):
    if t > 400:
        return 3
    if t > 200:
        return 6
    else:
        return 0


def random_policy(t):
    return random.randrange(7)


def greedy_policy(t):
    epsilon = 0.01
    if random.random() < epsilon:
        return random.randrange(7)
    else:
        best_percent = 0
        best_arm = 0
        for arm_id in range(7):
            percent = History.get_win_percent(arm_id)
            if percent > best_percent:
                best_percent = percent
                best_arm = arm_id
        return arm_id


def play(t, machine_id):
    if t > 400:
        if machine_id == 0:
            return random.random() < 0.1
        elif machine_id == 1:
            return random.random() < 0.3
        elif machine_id == 2:
            return random.random() < 0.5
        elif machine_id == 3:
            return random.random() < 0.9
        elif machine_id == 4:
            return random.random() < 0.6
        elif machine_id == 5:
            return random.random() < 0.4
        elif machine_id == 6:
            return random.random() < 0.2
    elif t > 200:
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


if __name__ == "__main__":
    main()
