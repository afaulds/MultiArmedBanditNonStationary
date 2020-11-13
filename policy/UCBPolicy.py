import random

class UCBPolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        print("NOT IMPLEMENTED")

    def get_arm(self, t):
        return random.randrange(self.num_machines)
