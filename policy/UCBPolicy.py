import random

class UCBPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        print("NOT IMPLEMENTED")

    def set_params(self, params):
        pass

    def get_arm(self, t):
        return random.randrange(self.num_machines)

    def store(self, t, arm_id, reward):
        pass

    def get_name(self):
        return "UCB"
