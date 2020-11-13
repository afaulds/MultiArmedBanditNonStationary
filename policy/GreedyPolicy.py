import random
from History import History

class GreedyPolicy:

    def __init__(self, machine_obj):
        self.num_machines = machine_obj.get_num_machines()
        self.epsilon = 0.05

    def get_arm(self, t):
        if random.random() < self.epsilon:
            return random.randrange(self.num_machines)
        else:
            best_percent = 0
            best_arm = 0
            for arm_id in range(self.num_machines):
                percent = History.get_win_percent(arm_id)
                if percent > best_percent:
                    best_percent = percent
                    best_arm = arm_id
            return best_arm
