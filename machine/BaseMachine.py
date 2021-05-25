from abc import ABC, abstractmethod


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

    @abstractmethod
    def play(self, t, arm_id):
        """
        Plays an arm at a certain time and returns
        whether there is a payout for this arm.

        t: int - Time step
        arm_id: int - Which arm id was pulled
        """
        pass

    @abstractmethod
    def oracle(self, t):
        """
        In order to calculate regret, we need an oracle to
        view inside the machine and indicate

        t: int - Time step
        """
        return 1

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

