from policy.BasePolicy import BasePolicy
import numpy as np


class Exp3Policy(BasePolicy):
    """

    """

    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.w = [1] * self.num_arms
        self.p = [0] * self.num_arms
        self.params = {
            "gamma": 0.3,
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_arms):
            value = self.p[arm_id]
            if value > best_value:
                best_value = value
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        W = 0
        for j in range(self.num_arms):
            W += self.w[j]

        for j in range(self.num_arms):
            self.p[j] = (1 - self.params["gamma"]) * self.w[j] / W + self.params["gamma"] / self.num_arms
            if j == arm_id:
                reward_carrot = reward / self.p[j]
            else:
                reward_carrot = 0
            x_carrot = reward / self.p[j]
            self.w[j] = self.w[j] * np.exp(self.params["gamma"] * reward_carrot / self.num_arms)

    def get_name(self):
        return "Exp3"
