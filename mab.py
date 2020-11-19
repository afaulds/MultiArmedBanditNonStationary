import random
from History import History
from machine import MachineManager
from policy import PolicyManager
import policy
from utils import Timer


force_policy_test = [
    "DiscountedThompsonSamplingPolicy",
    "DiscountedOptimisticThompsonSamplingPolicy",
    "DynamicThompsonSamplingPolicy",
#    "REXP3Policy",
    "RecurringMemoryThompsonSamplingPolicy",
    "ThompsonSamplingPolicy",
]
force_machine_test = None
[
    "AbruptVaryingMachine",
    "FastVaryingMachine",
    "SlowVaryingMachine",
]


def main():
    pm = PolicyManager()
    mm = MachineManager()
    for machine_name in force_machine_test or mm.get_machine_names():

        # Initialize for machine.
        mm.use(machine_name)
        h = History()

        # Deteremine dynamic oracle.
        for t in range(1, 5000):
            arm_id = mm.oracle(t)
            reward = mm.play(t, arm_id)
            h.store_oracle(t, arm_id, reward)

        for policy_name in force_policy_test or pm.get_policy_names():
            # Run policy for machine

            # Initialize policy
            Timer.start(policy_name)
            pm.use(policy_name, mm.get_num_machines())
            set_optimal_params(machine_name, policy_name, pm)
            h.reset()

            # Loop getting arm, playing machine, saving reward
            for t in range(1, 5000):
                arm_id = pm.get_arm(t)
                reward = mm.play(t, arm_id)
                pm.store(t, arm_id, reward)
                h.store(t, arm_id, reward)

            # Print results of run
            h.print(mm.get_name(), pm.get_name())
            Timer.stop(policy_name)


def set_optimal_params(machine_name, policy_name, pm):
    if machine_name == "AbruptVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
               "c": 50,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
               "gamma": 0.6,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.6,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.6,
                "period": 250,
            })
    if machine_name == "FastVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
               "c": 25,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
               "gamma": 0.4,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.4,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.4,
                "period": 100,
            })
    elif machine_name == "SlowVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 250,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.8,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.8,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.4,
                "period": 1000,
            })

if __name__ == "__main__":
    main()
