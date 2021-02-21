from abc import ABC, abstractmethod


class BasePolicy(ABC):
    """
    This implements a required format for policies.
    """
    @abstractmethod
    def __init__(self, num_machines):
        """
        Initialize a policy.

        num_machines: int - Number of machines to choose from.
        """
        pass

    @abstractmethod
    def set_params(self, params):
        """
        Allows us to set custom parameters for each policy.

        params: dict - Object containing custom parameters
        """
        pass

    @abstractmethod
    def get_arm(self, t):
        """
        Call to enact the policy and determine which arm to
        pull at time t. This is where the policy action is
        determined.

        t: int - Time step
        """
        return 0

    @abstractmethod
    def store(self, t, arm_id, reward):
        """
        Call to store information about what was played and
        the reward or payout for the play at a particular
        time step.

        t: int - Time step
        arm_id: int - Which arm id was pulled
        reward: int - 0 if no reward, 1 if reward is paid
        """
        pass

    @abstractmethod
    def get_name(self):
        """
        Get the name of the policy.
        """
        return ""

