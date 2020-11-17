import random


class StaticMachine:

    def __init__(self):
        pass

    def play(self, t, arm_id):
        if arm_id == 0:
            return 1.0 * (random.random() < 0.8)
        elif arm_id == 1:
            return 1.0 * (random.random() < 0.9)
        elif arm_id == 2:
            return 1.0 * (random.random() < 0.8)
        elif arm_id == 3:
            return 1.0 * (random.random() < 0.4)

    def oracle(self, t):
        return 1

    def get_num_machines(self):
        return 4

    def get_name(self):
        return 'Static'
