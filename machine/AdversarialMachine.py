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

    def get_probability(self, t, arm_id):
        probability = 0
        if arm_id == self.best_arm_id:
            probability = 0.8
        else:
            probability = 0.3
        if probability > 0.5:
            self.num_wins += 1
        if self.num_wins > self.max_wins:
            self.num_wins = 0
            self.best_arm_id = (self.best_arm_id + 1) % self.get_num_arms()
        return probability

    def get_num_arms(self):
        return 4

    def get_name(self):
        return "Adversarial"
