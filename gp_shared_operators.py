from math import cos, sin
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
