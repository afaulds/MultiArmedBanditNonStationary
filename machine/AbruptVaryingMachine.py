import random

class AbruptVaryingMachine:

    def __init__(self):
        self.start_time = -1
        self.section = 0

    def play(self, t, arm_id):
        if t > self.section:
            self.start_time = random.randrange(50) + self.section
            self.section += 250
        if arm_id == 0:
            if t < self.start_time:
                return 0.0
            else:
                return 0.1
        elif arm_id == 1:
            if t < self.start_time + 50:
                return 0.0
            else:
                return 0.3
        elif arm_id == 2:
            if t < self.start_time + 100:
                return 0.0
            else:
                return 0.6
        elif arm_id == 3:
            if t < self.start_time + 150:
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
