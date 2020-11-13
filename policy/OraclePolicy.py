import random

class OraclePolicy:

    def __init__(self, machine_obj):
        self.machine_obj = machine_obj

    def get_arm(self, t):
        return self.machine_obj.oracle(t)
