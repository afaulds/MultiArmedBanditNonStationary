import random

class REXP3Policy:

    def __init__(self, num_machines):
        self.num_machines = num_machines
        self.params = {
            "gamma": 0.6,
            "delta_t": 25,
        }

    def set_params(self, params):
        self.params.update(params)

    def get_arm(self, t):
        return random.randrange(self.num_machines)

    def store(self, t, arm_id, reward):
        pass

    def get_name(self):
        return "Random"
