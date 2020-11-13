print('a')
from policy.RandomPolicy import RandomPolicy
from policy.GreedyPolicy import GreedyPolicy
from policy.OraclePolicy import OraclePolicy
from policy.ThompsonSamplingPolicy import ThompsonSamplingPolicy
print('b')
import sys, os
print('c')

def getClasses(sub_dir):
    classes = {}
    #oldcwd = os.getcwd()
    #os.chdir(directory)   # change working directory so we know import will work
    for filename in os.listdir(sub_dir):
        if filename.endswith(".py"):
            modname = filename[:-3]
            classes[modname] = getattr(__import__(sub_dir + '.' + modname), modname)
    #os.setcwd(oldcwd)
    print(classes)
    print("")
    return classes

print('d')
globals().update(getClasses('policy'))
print('e')
