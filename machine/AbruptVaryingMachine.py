import random

class AbruptVaryingMachine:

    def __init__(self):
        pass

    def play(self, t, arm_id):
        t_adjusted = t % 250
        if arm_id == 0:
            if t_adjusted < 50:
                return 0.0
            else:
                return 0.1
        elif arm_id == 1:
            if t_adjusted < 100:
                return 0.0
            else:
                return 0.37
        elif arm_id == 2:
            if t_adjusted < 150:
                return 0.0
            else:
                return 0.63
        elif arm_id == 3:
            if t_adjusted < 250:
                return 0.0
            else:
                return 0.9

    def oracle(self, t):
        best_arm_id = 0
        best_value = 0
        for i in range(self.get_num_machines()):
            value = self.play(t, i)
            if value > best_value:
                best_value = value
                best_arm_id = i
        return best_arm_id

    def get_num_machines(self):
        return 4

    def get_name(self):
        return 'AbruptVarying'
