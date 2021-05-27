from machine.BaseMachine import BaseMachine
import math


class SlowVaryingMachine(BaseMachine):
    """
    Periodic machine that varies slowly.

    time: 0 - 250
       best arm: 0
       rewards: >85%
    time: 250 - 500
       best arm: 1
       rewards: >85%
    time: 500 - 750
       best arm: 2
       rewards: >85%
    time: 750 - 1000
       best arm: 3
       rewards: >85%
    repeat
    """

    def __init__(self):
        pass

    def get_probability(self, t, arm_id):
        if arm_id == 0:
            return 0.5 * math.sin((t + 125) * (2 * math.pi) / 1000) + 0.5
        elif arm_id == 1:
            return 0.5 * math.sin((t + 375) * (2 * math.pi) / 1000) + 0.5
        elif arm_id == 2:
            return 0.5 * math.sin((t + 625) * (2 * math.pi) / 1000) + 0.5
        elif arm_id == 3:
            return 0.5 * math.sin((t + 875) * (2 * math.pi) / 1000) + 0.5

    def get_num_arms(self):
        return 4

    def get_name(self):
        return "SlowVarying"
