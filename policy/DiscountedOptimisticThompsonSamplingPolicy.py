from policy.BasePolicy import BasePolicy
import numpy as np
from scipy.stats import beta


class DiscountedOptimisticThompsonSamplingPolicy(BasePolicy):
    """
    Similar to Discounted Thompson Sampling, this includes
    mean or expected as a factor in selection. Always picks
    mean or higher in the beta distribution.
    """

    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.a = [1] * self.num_arms
        self.b = [1] * self.num_arms
        self.params = {
            "gamma": 0.6,
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_arms):
            value = np.random.beta(self.a[arm_id], self.b[arm_id])
            value = max(value, self.a[arm_id] / (self.a[arm_id] + self.b[arm_id]))
            if value > best_value:
                best_value = value
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        for i in range(self.num_arms):
            self.a[i] = self.params["gamma"] * self.a[i]
            self.b[i] = self.params["gamma"] * self.b[i]
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)

    def get_name(self):
        return "dOTS (\u03B3={})".format(self.params["gamma"])
