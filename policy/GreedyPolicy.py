import random

class GreedyPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.epsilon = 0.05
        self.a = [0] * self.num_machines
        self.b = [0] * self.num_machines

    def get_arm(self, t):
        if random.random() < self.epsilon:
            return random.randrange(self.num_machines)
        else:
            best_percent = 0
            best_arm = 0
            for arm_id in range(self.num_machines):
                if self.a[arm_id] == 0:
                    percent = 0
                else:
                    percent = 1.0 * self.a[arm_id] / (self.a[arm_id] + self.b[arm_id])
                if percent > best_percent:
                    best_percent = percent
                    best_arm = arm_id
            return best_arm

    def store(self, t, arm_id, reward):
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)
