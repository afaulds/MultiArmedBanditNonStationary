from machine.BaseMachine import BaseMachine
import math


class FastVaryingMachine(BaseMachine):
    """
    Periodic machine that varies quickly.

    time: 0 - 25
       best arm: 0
       rewards: >85%
    time: 25 - 50
       best arm: 1
       rewards: >85%
    time: 50 - 75
       best arm: 2
       rewards: >85%
    time: 75 - 100
       best arm: 3
       rewards: >85%
    repeat
    """

    def __init__(self):
        pass

    def play(self, t, arm_id):
        if arm_id == 0:
            return 0.5 * math.sin((t + 12.5) * (2 * math.pi) / 100) + 0.5
        elif arm_id == 1:
            return 0.5 * math.sin((t + 37.5) * (2 * math.pi) / 100) + 0.5
        elif arm_id == 2:
            return 0.5 * math.sin((t + 62.5) * (2 * math.pi) / 100) + 0.5
        elif arm_id == 3:
            return 0.5 * math.sin((t + 87.5) * (2 * math.pi) / 100) + 0.5

    def oracle(self, t):
        best_arm_id = 0
        best_value = 0
        for i in range(self.get_num_arms()):
            value = self.play(t, i)
            if value > best_value:
                best_value = value
                best_arm_id = i
        return best_arm_id

    def get_num_arms(self):
        return 4

    def get_name(self):
        return 'FastVarying'
