import numpy as np
import random


class DynamicThompsonSamplingPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.c = 50
        self.a = [0] * self.num_machines
        self.b = [0] * self.num_machines

    def get_arm(self, t):
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_machines):
            value = np.random.beta(self.a[arm_id] + 1, self.b[arm_id] + 1)
            if value > best_value:
                best_value = value
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        if self.a[arm_id] + self.b[arm_id] > self.c:
            self.a[arm_id] = (self.a[arm_id] + reward) * self.c / (self.c + 1)
            self.b[arm_id] = (self.b[arm_id] + (1 - reward)) * self.c / (self.c + 1)
        else:
            self.a[arm_id] = self.a[arm_id] + reward
            self.b[arm_id] = self.b[arm_id] + (1 - reward)

    def get_name(self):
        return 'DTS (c={})'.format(self.c)
