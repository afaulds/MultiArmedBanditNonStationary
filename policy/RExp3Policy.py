from policy.BasePolicy import BasePolicy
import numpy as np


class RExp3Policy(BasePolicy):
    """

    """

    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.w = [1] * self.num_arms
        self.p = [1.0 / self.num_arms] * self.num_arms
        self.params = {
            "gamma": 0.5,
            "period": 5,
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
        if t % self.params["period"] == 1:
            self.w = [1] * self.num_arms
        reward_tilde = reward/self.p[arm_id]
        self.w[arm_id] = self.w[arm_id] * np.exp(self.params["gamma"]*reward_tilde / self.num_arms)
        for i in range(self.num_arms):
            self.p[i] = (1 - self.params["gamma"]) * self.w[i] / np.sum(self.w) + self.params["gamma"] / self.num_arms

    def get_name(self):
        return "REXP3"
