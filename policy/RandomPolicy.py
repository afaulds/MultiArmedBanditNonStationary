from policy.BasePolicy import BasePolicy
import random


class RandomPolicy(BasePolicy):

    def __init__(self, num_arms):
        self.num_arms = num_arms

    def set_params(self, params):
        pass

    def get_arm(self, t):
        return random.randrange(self.num_arms)

    def store(self, t, arm_id, reward):
        pass

    def get_name(self):
        return "Random"
