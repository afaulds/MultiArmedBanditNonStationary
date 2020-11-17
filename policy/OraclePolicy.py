import random

class OraclePolicy:

    def __init__(self, num_machines):
        self.num_machines = num_machines

    def get_arm(self, t):
        return -1

    def store(self, t, arm_id, reward):
        pass

    def get_name(self):
        return 'Oracle'
