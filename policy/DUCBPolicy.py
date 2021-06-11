from policy.BasePolicy import BasePolicy
import numpy as np


class DUCBPolicy(BasePolicy):
    """
    Similar to greedy but includes an upper confidence bound
    that is the exploration element. It reduces as the arm is
    played enough and as all arms play.

    sqrt(2 * ln t / Na(t))
    t - Number of overall plays
    Na(t) - Number of plays on arm a
    """

    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.a = [1] * self.num_arms
        self.n = [1] * self.num_arms
        self.c = [1] * self.num_arms
        self.params = {
            "gamma": 0.992,
            "zeta": 0.6,
            "B": 1,
        }

    def set_params(self, params):
        pass

    def get_arm(self, t):
        best_ucb = 0
        best_arm = 0
        for arm_id in range(self.num_arms):
            ucb = 1.0 * self.a[arm_id] / self.n[arm_id]
            ucb += self.c[arm_id]
            if ucb > best_ucb:
                best_ucb = ucb
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        for i in range(self.num_arms):
            self.a[i] *= self.params["gamma"]
            self.n[i] *= self.params["gamma"]
        self.a[arm_id] += reward
        self.n[arm_id] += 1
        n_total = np.sum(self.n)
        for i in range(self.num_arms):
            self.c[i] = 2 * self.params["B"] * np.sqrt(self.params["zeta"] * np.log(n_total) / self.n[i])

    def get_name(self):
        return "DUCB (\u03B3={})".format(self.params["gamma"])
