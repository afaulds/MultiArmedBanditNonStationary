import random


class TestMachine:

    def __init__(self):
        pass

    def play(self, t, arm_id):
        if t > 4000:
            if arm_id == 0:
                return 1.0 * (random.random() < 0.1)
            elif arm_id == 1:
                return 1.0 * (random.random() < 0.3)
            elif arm_id == 2:
                return 1.0 * (random.random() < 0.5)
            elif arm_id == 3:
                return 1.0 * (random.random() < 0.9)
        elif t > 2000:
            if arm_id == 0:
                return 1.0 * (random.random() < 0.1)
            elif arm_id == 1:
                return 1.0 * (random.random() < 0.9)
            elif arm_id == 2:
                return 1.0 * (random.random() < 0.3)
            elif arm_id == 3:
                return 1.0 * (random.random() < 0.4)
        else:
            if arm_id == 0:
                return 1.0 * (random.random() < 0.9)
            elif arm_id == 1:
                return 1.0 * (random.random() < 0.6)
            elif arm_id == 2:
                return 1.0 * (random.random() < 0.5)
            elif arm_id == 3:
                return 1.0 * (random.random() < 0.4)

    def oracle(self, t):
        if t > 4000:
            return 3
        elif t > 2000:
            return 1
        else:
            return 0

    def get_num_machines(self):
        return 4

    def get_name(self):
        return 'Test'
