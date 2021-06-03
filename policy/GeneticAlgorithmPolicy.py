from policy.BasePolicy import BasePolicy
import numpy as np
import warnings


class GeneticAlgorithmPolicy(BasePolicy):
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.a = [1] * self.num_arms
        self.b = [1] * self.num_arms
        self.params = {
            "eq_str": "0",
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        tie_breaker = 0.00000001 * np.random.random_sample()
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_arms):
            value = self.__evaluate(
                self.a[arm_id],
                self.b[arm_id],
                self.a[arm_id] + self.b[arm_id],
                t
            ) + tie_breaker
            if value >= best_value:
                best_value = value
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        self.a[arm_id] = self.a[arm_id] + reward
        self.b[arm_id] = self.b[arm_id] + (1 - reward)

    def get_name(self):
        return "GeneticAlgorithm"

    def __evaluate(self, a, b, n, t):
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            return eval(self.params["eq_str"])
        except:
            return 1

