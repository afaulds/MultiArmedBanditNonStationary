from machine.BaseMachine import BaseMachine
import random


class StaticMachine(BaseMachine):
    """
    This is a machine that one arm pays out
    more than the other arms through all time. The
    best arm is static.

    time: 0 - ???
       best arm: 1
       rewards: 90%
    """

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

    def get_num_arms(self):
        return 4

    def get_name(self):
        return "Static"
