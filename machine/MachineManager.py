import os


class MachineManager:
    """
    This allows for dynamic plug-n-play of all machines.
    By adding machines to the machine directory and ending
    the name with Machine.py and inheriting from BaseMachine,
    this class automatically reads the policy and allows it
    to be called.
    """

    def __init__(self):
        self.machine_names = self.get_machine_list()
        self.machine = ""
        self.load_classes()

    def get_machine_list(self):
        names = []
        for filename in os.listdir("machine"):
            if filename.endswith("Machine.py") and not filename.endswith("BaseMachine.py"):
                names.append(filename[:-3])
        return names

    def load_classes(self):
        self.classes = {}
        modnames = self.get_machine_list()
        for modname in modnames:
            self.classes[modname] = getattr(__import__("machine." + modname), modname)

    def get_machine_names(self):
        return self.machine_names

    def use(self, name):
        self.machine = eval("self.classes[name].{}()".format(name))

    def play(self, t, arm_id):
        return self.machine.play(t, arm_id)

    def oracle(self, t):
        return self.machine.oracle(t)

    def set_num_arms(self, num_arms):
        return self.machine.set_num_arms(num_arms)

    def get_num_arms(self):
        return self.machine.get_num_arms()

    def get_name(self):
        return self.machine.get_name()
