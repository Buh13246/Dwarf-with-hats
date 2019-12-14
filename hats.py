"""A Dwarf with hats Module.

This module provides a solution(x) function
which returns a list of ints whether the dwarf has a hat or not.
"""

__all__ = ['solution']
__version__ = '0.1'
__author__ = 'Philipp Wellner'

import threading
from time import sleep
# default start can also be empty.
hats = [1, 0, 0, 1, 0, 0, 0, 0, 1, 0]

# prevents that two threads calculates the same result
calculating_lock = threading.Lock()

def solution(x=10):
    """returns a list of x ints whether the dwarf has a hat or not
    """
    # last is maybe not correct and is still calculated in another Thread
    if len(hats) > x:
        return hats[:x]
    # lock if no thread is calculating right now
    while not calculating_lock.acquire(False):
        sleep(0.1)
        # still locked but maybe the other thread did my work
        if len(hats) > x:
            return hats[:x]
    for current_dwarf in range(len(hats), x+1):
        # init default
        hats.append(1)
        for ii in range(2, current_dwarf+2):
            if (current_dwarf + 1) % ii == 0:
                # using Bit Operations
                hats[current_dwarf] ^= 1
        # reset all other bits to 0
        hats[current_dwarf] &= 1
    calculating_lock.release()
    return hats[:x]
