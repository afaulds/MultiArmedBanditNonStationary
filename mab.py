import random
from History import History
from machine import MachineManager
from policy import PolicyManager
import policy
from utils import Timer


force_policy_test = None
force_machine_test = ['SlowVaryingMachine']


def main():
    pm = PolicyManager()
    mm = MachineManager()
    for policy_name in force_policy_test or pm.get_policy_names():
        for machine_name in force_machine_test or mm.get_machine_names():
            Timer.start(policy_name)
            History.init()
            mm.use(machine_name)
            pm.use(policy_name, mm.get_num_machines())
            for t in range(1, 5000):
                if policy_name == 'OraclePolicy':
                    arm_id = mm.oracle(t)
                else:
                    arm_id = pm.get_arm(t)
                reward = mm.play(t, arm_id)
                pm.store(t, arm_id, reward)
                History.store(t, arm_id, reward)
            History.print(machine_name, policy_name)
            Timer.stop(policy_name)


if __name__ == "__main__":
    main()
