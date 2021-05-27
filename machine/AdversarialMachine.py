from machine.BaseMachine import BaseMachine
import math
import random


class AdversarialMachine(BaseMachine):
    """

    """

    def __init__(self):
        self.best_arm_id = 0
        self.max_wins = 200
        self.num_wins = 0
        pass

    def play(self, t, arm_id):
        result = 0
        if arm_id == self.best_arm_id:
            result = 0.8
        else:
            result = 0.3
        if result > 0.5:
            self.num_wins += 1
        if self.num_wins > self.max_wins:
            self.num_wins = 0
            self.best_arm_id = (self.best_arm_id + 1) % self.get_num_arms()
        return result

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
        return "Adversarial"
