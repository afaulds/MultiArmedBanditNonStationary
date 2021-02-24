from policy.BasePolicy import BasePolicy
import random


class GreedyPolicy(BasePolicy):
    """
    Greedy policy plays the arm with the best probability.
    It uses exploration epsilon percent of the time to find
    a new better arm, otherwise it only plays the best arm.
    """

    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.a = [0] * self.num_arms
        self.b = [0] * self.num_arms
        self.params = {
            "epsilon": 0.05,
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        if random.random() < self.params["epsilon"]:
            return random.randrange(self.num_arms)
        else:
            best_percent = 0
            best_arm = 0
            for arm_id in range(self.num_arms):
                if self.a[arm_id] == 0:
                    percent = 0
                else:
                    percent = 1.0 * self.a[arm_id] / (self.a[arm_id] + self.b[arm_id])
                if percent > best_percent:
                    best_percent = percent
                    best_arm = arm_id
            return best_arm

    def store(self, t, arm_id, reward):
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)

    def get_name(self):
        return "Greedy (\u03B5={})".format(self.params["epsilon"])
