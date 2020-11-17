import random
import numpy as np
from History import History

class REXP3Policy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.gamma = 0.3593

    def set_params(self, params):
        pass

    def get_arm(self, t):
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_machines):
            a = History.get_win_count(arm_id)
            b = History.get_loss_count(arm_id)
            value = np.random.beta(a + 1, b + 1)
            if value > best_value:
                best_value = value
                best_arm = arm_id
        return best_arm

    def store(self, t, arm_id, reward):
        pass

    def get_name(self):
        return "REXP3 (\u03B3=)".format(self.gamma)
