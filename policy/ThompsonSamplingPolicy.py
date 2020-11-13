import random
import numpy as np
from History import History

class ThompsonSamplingPolicy:

    def __init__(self, machine_obj):
        self.num_machines = machine_obj.get_num_machines()

    def get_arm(self, t):
        best_value = 0
        best_arm = 0
        for arm_id in range(self.num_machines):
            a = History.get_win_count(arm_id)
            b = History.get_loss_count(arm_id)
            value = np.random.beta(a, b)
            if value > best_value:
                best_value = value
                best_arm = arm_id
        return best_arm
