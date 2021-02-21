from policy.BasePolicy import BasePolicy
import numpy as np


class DiscountedThompsonSamplingPolicy(BasePolicy):

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.a = [0] * self.num_machines
        self.b = [0] * self.num_machines
        self.params = {
            "gamma": 0.6,
        }

    def set_params(self, params):
        self.params.update(params)

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
        value = np.random.uniform(0, 1)
        if value < reward:
            reward = 1
        else:
            reward = 0
        for i in range(self.num_machines):
            self.a[i] = self.params["gamma"] * self.a[i]
            self.b[i] = self.params["gamma"] * self.b[i]
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)

    def get_name(self):
        return "dTS (\u03B3={})".format(self.params["gamma"])
