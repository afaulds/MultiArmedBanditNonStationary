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
        self.payout = []
        self.set_num_arms(4)

    def get_probability(self, t, arm_id):
        return self.payout[arm_id]

    def set_num_arms(self, num_arms):
        ids = list(range(num_arms))
        random.shuffle(ids)
        self.payout = [0] * num_arms
        for i in range(num_arms):
            self.payout[ids[i]] = 0.1 + 0.8 * i / num_arms

    def get_num_arms(self):
        return len(self.payout)

    def get_name(self):
        return "Static"
