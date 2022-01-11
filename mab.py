from History import History
from machine import MachineManager
from policy import PolicyManager
import policy
from utils import Settings
from utils import Timer


T = 5000 # Max time


def main():
    """
    Main loop to run through all combinations
    of machines and policies.
    """

    # Initialize objects that are plug-n-play for different policies and machines
    pm = PolicyManager()
    mm = MachineManager()

    # Loop through all machines
    for machine_name in Settings.get_value("machine_list") or mm.get_machine_names():

        # Initialize for machine.
        mm.use(machine_name)
        h = History()

        # Deteremine dynamic oracle.
        for t in range(1, T):
            arm_id, prob = mm.oracle(t)
            h.store_oracle(t, arm_id, prob)

        # Loop through all policies
        for policy_name in Settings.get_value("policy_list") or pm.get_policy_names():
            # Run policy for machine

            # Initialize policy
            Timer.start(policy_name)
            pm.use(policy_name, mm.get_num_arms())
            set_optimal_params(machine_name, policy_name, pm)
            h.reset()

            # Loop getting arm, playing machine, saving reward
            for t in range(1, T):
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
               "c": 1,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
               "gamma": 0.963,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.984,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.992,
                "period": 250,
            })
        elif policy_name == "GeneticProgrammingPolicy":
            pm.set_params({
                #BESTOVERALL"eq_str": "protected_div(protected_sqrt(add(min(mul(protected_log(b), min(b, max(t, t))), n), max(t, mul(b, b)))), min(mul(b, protected_sqrt(add(b, sigmoid(protected_sqrt(min(mul(b, protected_sqrt(add(b, b))), b)))))), b))"
                #UCB"eq_str": "protected_div(a, a + b) + protected_sqrt(2 * np.log(t) / (a + b))"
                #BESTINDIVIDUAL
                "eq_str": "protected_div(add(max(n, b), b), mul(b, b))"
            })
    if machine_name == "FastVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
               "c": 2,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
               "gamma": 0.898,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.943,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.951,
                "period": 100,
            })
        elif policy_name == "GeneticProgrammingPolicy":
            pm.set_params({
                #BESTOVERALL"eq_str": "protected_div(protected_sqrt(add(min(mul(protected_log(b), min(b, max(t, t))), n), max(t, mul(b, b)))), min(mul(b, protected_sqrt(add(b, sigmoid(protected_sqrt(min(mul(b, protected_sqrt(add(b, b))), b)))))), b))"
                #UCB"eq_str": "protected_div(a, a + b) + protected_sqrt(2 * np.log(t) / (a + b))"
                #BESTINDIVIDUAL"eq_str": "sub(t, max(b, protected_beta(t, min(b, a))))"
                "eq_str": "t-b"
            })
    elif machine_name == "SlowVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 5,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.976,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.992,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.992,
                "period": 1000,
            })
        elif policy_name == "GeneticProgrammingPolicy":
            pm.set_params({
                #BESTOVERALL"eq_str": "protected_div(protected_sqrt(add(min(mul(protected_log(b), min(b, max(t, t))), n), max(t, mul(b, b)))), min(mul(b, protected_sqrt(add(b, sigmoid(protected_sqrt(min(mul(b, protected_sqrt(add(b, b))), b)))))), b))"
                #UCB"eq_str": "protected_div(a, a + b) + protected_sqrt(2 * np.log(t) / (a + b))"
                #BESTINDIVIDUAL
                "eq_str": "protected_div(max(max(b, add(max(max(add(t, a), b), a), a)), add(max(max(add(t, a), t), add(add(max(b, max(add(t, a), t)), neg(b)), a)), a)), b)"
            })
    elif machine_name == "StaticMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 2,
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
                "gamma": 1.0,
                "period": 1000,
            })
        elif policy_name == "GeneticProgrammingPolicy":
            pm.set_params({
                #BESTOVERALL"eq_str": "protected_div(protected_sqrt(add(min(mul(protected_log(b), min(b, max(t, t))), n), max(t, mul(b, b)))), min(mul(b, protected_sqrt(add(b, sigmoid(protected_sqrt(min(mul(b, protected_sqrt(add(b, b))), b)))))), b))"
                #UCB"eq_str": "protected_div(a, a + b) + protected_sqrt(2 * np.log(t) / (a + b))"
                #BESTINDIVIDUAL
                "eq_str": "add(protected_sqrt(a), sub(a, b))"
            })
    elif machine_name == "NonCycleVaryingMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 2,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.996,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.996,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.996,
                "period": 5000,
            })
        elif policy_name == "GeneticProgrammingPolicy":
            pm.set_params({
                #BESTOVERALL"eq_str": "protected_div(protected_sqrt(add(min(mul(protected_log(b), min(b, max(t, t))), n), max(t, mul(b, b)))), min(mul(b, protected_sqrt(add(b, sigmoid(protected_sqrt(min(mul(b, protected_sqrt(add(b, b))), b)))))), b))"
                #UCB"eq_str": "protected_div(a, a + b) + protected_sqrt(2 * np.log(t) / (a + b))"
                #BESTINDIVIDUAL
                "eq_str": "protected_div(protected_div(protected_sqrt(min(a, n)), protected_beta(t, min(min(a, n), n))), b)"
            })
    elif machine_name == "AdversarialMachine":
        if policy_name == "DynamicThompsonSamplingPolicy":
            pm.set_params({
                "c": 2,
            })
        elif policy_name == "DiscountedThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.984,
            })
        elif policy_name == "DiscountedOptimisticThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.992,
            })
        elif policy_name == "RecurringMemoryThompsonSamplingPolicy":
            pm.set_params({
                "gamma": 0.992,
                "period": 800,
            })
        elif policy_name == "GeneticProgrammingPolicy":
            pm.set_params({
                #BESTOVERALL"eq_str": "protected_div(protected_sqrt(add(min(mul(protected_log(b), min(b, max(t, t))), n), max(t, mul(b, b)))), min(mul(b, protected_sqrt(add(b, sigmoid(protected_sqrt(min(mul(b, protected_sqrt(add(b, b))), b)))))), b))"
                #UCB"eq_str": "protected_div(a, a + b) + protected_sqrt(2 * np.log(t) / (a + b))"
                #BESTINDIVIDUAL
                "eq_str": "protected_div(a + 2 * b, b * b)"
            })


if __name__ == "__main__":
    main()
