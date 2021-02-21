from policy.BasePolicy import BasePolicy
import random

class REXP3Policy(BasePolicy):

    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.params = {
            "gamma": 0.6,
            "delta_t": 25,
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        return random.randrange(self.num_arms)

    def store(self, t, arm_id, reward):
        pass

    def get_name(self):
        return "Random"
