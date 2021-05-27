from abc import ABC, abstractmethod
import random


class BaseMachine(ABC):
    """
    This implements a required format for machines.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize a machine.
        """
        pass

    def play(self, t, arm_id):
        """
        Plays an arm at a certain time and returns
        whether there is a payout for this arm.

        t: int - Time step
        arm_id: int - Which arm id was pulled
        """
        probability = self.get_probability(t, arm_id)
        reward = 0
        if random.random() < probability:
            reward = 1
        return reward

    @abstractmethod
    def get_probability(self, t, arm_id):
        """
        Gets the Bernoulli probability for
        an arm at a certain time and returns
        the probability.

        t: int - Time step
        arm_id: int - Which arm id was pulled
        """
        pass

    def oracle(self, t):
        """
        In order to calculate regret, we need an oracle to
        view inside the machine and indicate

        t: int - Time step
        """
        best_arm_id = 0
        best_prob = 0
        for i in range(self.get_num_arms()):
            prob = self.get_probability(t, i)
            if prob > best_prob:
                best_prob = prob
                best_arm_id = i
        return best_arm_id, best_prob

    @abstractmethod
    def get_num_arms(self):
        """
        Get the number of arms for this machine.
        """
        return 0

    @abstractmethod
    def get_name(self):
        """
        Get the name of the machine.
        """
        return ""

