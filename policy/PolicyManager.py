import sys, os


class PolicyManager:

    def __init__(self):
        self.policy_names = self.get_policy_list()
        self.policy = ''
        self.load_classes()

    def get_policy_list(self):
        names = []
        for filename in os.listdir('policy'):
            if filename.endswith('Policy.py'):
                names.append(filename[:-3])
        return names

    def load_classes(self):
        self.classes = {}
        modnames = self.get_policy_list()
        for modname in modnames:
            self.classes[modname] = getattr(__import__('policy.' + modname), modname)

    def get_policy_names(self):
        return self.policy_names

    def use(self, name, num_machines):
        self.policy = eval("self.classes[name].{}(num_machines)".format(name))

    def get_arm(self, t):
        return self.policy.get_arm(t)

    def store(self, t, arm_id, reward):
        return self.policy.store(t, arm_id, reward)

    def get_name(self):
        return self.policy.get_name()
