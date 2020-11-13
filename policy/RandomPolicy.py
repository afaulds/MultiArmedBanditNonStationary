import random

class RandomPolicy:

    def __init__(self, machine_obj):
        self.num_machines = machine_obj.get_num_machines()

    def get_arm(self, t):
        return random.randrange(self.num_machines)
