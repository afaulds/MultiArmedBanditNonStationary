import os


class MachineManager:

    def __init__(self):
        self.machine_names = self.get_machine_list()
        self.machine = ''
        self.load_classes()

    def get_machine_list(self):
        names = []
        for filename in os.listdir('machine'):
            if filename.endswith("Machine.py"):
                names.append(filename[:-3])
        return names

    def load_classes(self):
        self.classes = {}
        modnames = self.get_machine_list()
        for modname in modnames:
            self.classes[modname] = getattr(__import__('machine.' + modname), modname)

    def get_machine_names(self):
        return self.machine_names

    def use(self, name):
        self.machine = eval("self.classes[name].{}()".format(name))

    def play(self, t, arm_id):
        return self.machine.play(t, arm_id)

    def oracle(self, t):
        return self.machine.oracle(t)

    def get_num_machines(self):
        return self.machine.get_num_machines()

    def get_name(self):
        return self.machine.get_name()
