import sys, os


class PolicyManager:
    """
    This allows for dynamic plug-n-play of all policies.
    By adding policies to the policy directory and ending
    the name with Policy.py and inheriting from BasePolicy,
    this class automatically reads the policy and allows it
    to be called.
    """

    def __init__(self):
        """
        Initialize policy manager
        """
        self.policy_names = self.__get_policy_list()
        self.policy = ""
        self.load_classes()

    def __get_policy_list(self):
        """
        Get an array of the names of all available policies.
        Private method that reads the policy directory.
        """
        names = []
        for filename in os.listdir("policy"):
            if filename.endswith("Policy.py") and not filename.endswith("BasePolicy.py"):
                names.append(filename[:-3])
        return names

    def load_classes(self):
        """
        Get all policies and dynamically load policy files.
        """
        self.classes = {}
        modnames = self.__get_policy_list()
        for modname in modnames:
            self.classes[modname] = getattr(__import__("policy." + modname), modname)

    def get_policy_names(self):
        """
        Get an array list of all available policies.
        """
        return self.policy_names

    def set_params(self, params):
        """
        Pass through method to call the current policy's set_params.

        params: dict - Dictionary of custom policy parameter values
        """
        self.policy.set_params(params)

    def use(self, name, num_arms):
        """
        Indicates which policy to start using. Select by name
        and indicate how many machines the policy can choose from.

        name: string - Name of the policy
        num_arms: int - Number of arms for the policy to choose from
        """
        self.policy = eval("self.classes[name].{}(num_arms)".format(name))

    def get_arm(self, t):
        """
        Pass through method to call current policy's get_arm.

        t: int - Time step
        """
        return self.policy.get_arm(t)

    def store(self, t, arm_id, reward):
        """
        Pass through method to call current policy's store.

        t: int - Time step
        arm_id: int - Which arm id was pulled
        reward: int - 0 if no reward, 1 if reward is paid
        """
        return self.policy.store(t, arm_id, reward)

    def get_name(self):
        """
        Pass through method to call current policy's get_name.
        """
        return self.policy.get_name()
