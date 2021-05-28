from policy.BasePolicy import BasePolicy
import numpy as np


class UCBPolicy(BasePolicy):
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
        self.a = [0] * self.num_arms
        self.b = [0] * self.num_arms

    def set_params(self, params):
        pass

    def get_arm(self, t):
        best_ucb = 0
        best_arm = 0
        for arm_id in range(self.num_arms):
            if self.a[arm_id] == 0:
                ucb = 0
                ucb += 9999.0
            else:
                ucb = 1.0 * self.a[arm_id] / (self.a[arm_id] + self.b[arm_id])
                ucb += np.sqrt(2 * np.log(t) / (self.a[arm_id] + self.b[arm_id]))
            if ucb > best_ucb:
                best_ucb = ucb
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)

    def get_name(self):
        return "UCB"
