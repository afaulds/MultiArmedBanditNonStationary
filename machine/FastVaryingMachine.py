import math

class FastVaryingMachine:

    def __init__(self):
        pass

    def play(self, t, arm_id):
        if arm_id == 0:
            return 0.5 * math.sin((t + 0) * (2 * math.pi) / 100) + 0.5
        elif arm_id == 1:
            return 0.5 * math.sin((t + 25) * (2 * math.pi) / 100) + 0.5
        elif arm_id == 2:
            return 0.5 * math.sin((t + 50) * (2 * math.pi) / 100) + 0.5
        elif arm_id == 3:
            return 0.5 * math.sin((t + 75) * (2 * math.pi) / 100) + 0.5

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
