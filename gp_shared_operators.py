from math import cos, sin, exp
import numpy as np
from operator import *
import random

def protected_div(x, y):
    if y == 0:
        return 1
    else:
        return x / y

def protected_sqrt(x):
    if x >= 0:
        return np.sqrt(x)
    else:
        return 0

def protected_log(x):
    if x > 0:
        return np.log(x)
    else:
        return 0

def protected_beta(a, b):
    if a <= 0 or b <= 0:
        return 1
    else:
        return np.random.beta(a, b)

def sigmoid(x):
    if x >= 0:
        z = exp(-x)
        sig = 1 / (1 + z)
        return sig
    else:
        z = exp(x)
        sig = z / (1 + z)
        return sig

def eq123(input, output1, output2, output3):
    if input == 1:
        return [output1]
    elif input == 2:
        return [output2]
    elif input == 3:
        return [output3]
    else:
        print(input)
        print("BROKEN")
        return []