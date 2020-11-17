import math
import numpy as np
import random


class RecurringMemoryThompsonSamplingPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.gamma = 0.6
        self.a = [0] * self.num_machines
        self.b = [0] * self.num_machines
        self.cycle_memory = []
        self.period = 1000

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
        for i in range(self.num_machines):
            self.a[i] = self.gamma * self.a[i]
            self.b[i] = self.gamma * self.b[i]
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)

        # Cycle memory
        if len(self.cycle_memory) > self.period:
            (arm_id, reward) = self.cycle_memory.pop(0)
        self.a[arm_id] += math.ceil(t / self.period) * reward
        self.b[arm_id] += math.ceil(t / self.period) * (1 - reward)
        self.cycle_memory.append((arm_id, reward))

    def get_name(self):
        return 'RMTS (T={})'.format(self.period)
