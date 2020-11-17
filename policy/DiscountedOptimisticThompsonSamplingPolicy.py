import random
from scipy.stats import beta
from History import History

class DiscountedOptimisticThompsonSamplingPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.a = [0] * self.num_machines
        self.b = [0] * self.num_machines
        self.beta_mean_cache = {}
        self.params = {
            "gamma": 0.6,
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_machines):
            value = beta.rvs(self.a[arm_id] + 1, self.b[arm_id] + 1)
            value = max(value, self.beta_mean(self.a[arm_id] + 1, self.b[arm_id] + 1))
            if value > best_value:
                best_value = value
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        for i in range(self.num_machines):
            self.a[i] = self.params["gamma"] * self.a[i]
            self.b[i] = self.params["gamma"] * self.b[i]
        self.a[arm_id] += reward
        self.b[arm_id] += (1 - reward)

    def beta_mean(self, a, b):
        key = "{}_{}".format(a, b)
        if key not in self.beta_mean_cache:
            self.beta_mean_cache[key] = beta.stats(a + 1, b + 1, moments="m")
        return self.beta_mean_cache[key]

    def get_name(self):
        return "dOTS (\u03B3={})".format(self.params["gamma"])
