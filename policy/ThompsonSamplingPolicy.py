import numpy as np
import random


class ThompsonSamplingPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.a = [0] * self.num_machines
        self.b = [0] * self.num_machines

    def set_params(self, params):
        pass

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
        self.a[arm_id] = self.a[arm_id] + reward
        self.b[arm_id] = self.b[arm_id] + (1 - reward)

    def get_name(self):
        return "TS"