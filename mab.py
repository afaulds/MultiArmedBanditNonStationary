import random
from History import History
from machine import MachineManager
from policy import PolicyManager
import policy
from utils import Timer


force_policy_test = None
[
    "DiscountedThompsonSamplingPolicy",
    "DiscountedOptimisticThompsonSamplingPolicy",
    "DynamicThompsonSamplingPolicy",
    "REXP3Policy",
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
    """
    Main loop to run through all combinations
    of machines and policies.
    """

    # Initialize objects that are plug-n-play for different policies and machines
    pm = PolicyManager()
    mm = MachineManager()

    # Loop through all machines
    for machine_name in force_machine_test or mm.get_machine_names():

        # Initialize for machine.
        mm.use(machine_name)
        h = History()

        # Deteremine dynamic oracle.
        for t in range(1, 5000):
            arm_id = mm.oracle(t)
            reward = mm.play(t, arm_id)
            h.store_oracle(t, arm_id, reward)

        # Loop through all policies
        for policy_name in force_policy_test or pm.get_policy_names():
            # Run policy for machine

            # Initialize policy
            Timer.start(policy_name)
            pm.use(policy_name, mm.get_num_arms())
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
    """
    Set optimal parameters for each run. These are precalculated
    to compare algorithms with the best results

    machine_name: string - Name of the machine
    policy_name: string - Name of the policy
    pm: PolicyManager - Used to set optimal parameters
    """
    if machine_name == "AbruptVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
               "c": 50,
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
                "gamma": 0.97,
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
                "gamma": 0.85,
                "period": 100,
            })
    elif machine_name == "SlowVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 250,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.98,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.98,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.98,
                "period": 1000,
            })
    elif machine_name == "StaticMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 250,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 1.0,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 1.0,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 1.00,
                "period": 5000,
            })
    elif machine_name == "TestMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 250,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 1.0,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 1.0,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 1.00,
                "period": 5000,
            })

if __name__ == "__main__":
    main()
