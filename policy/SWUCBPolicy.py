from policy.BasePolicy import BasePolicy
import numpy as np


class SWUCBPolicy(BasePolicy):
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
        self.cycle_memory = []
        self.params = {
            "zeta": 0.6,
            "tau": 100,
            "B": 1,
        }

    def set_params(self, params):
        pass

    def get_arm(self, t):
        best_ucb = 0
        best_arm = 0
        for arm_id in range(self.num_arms):
            ucb = 1.0 * self.a[arm_id] / self.n[arm_id]
            ucb += self.params["B"] * np.sqrt(self.params["zeta"] * np.log(min(t, self.params["tau"])) / (self.n[arm_id]))
            if ucb > best_ucb:
                best_ucb = ucb
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        self.a[arm_id] += reward
        self.n[arm_id] += 1

        self.cycle_memory.append((arm_id, reward))
        if len(self.cycle_memory) > self.params["tau"]:
            (arm_id, reward) = self.cycle_memory.pop(0)
            self.a[arm_id] -= reward
            self.n[arm_id] -= 1

    def get_name(self):
        return "SWUCB (\u03C4={})".format(self.params["tau"])
