# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
import threading
from time import sleep
# default start can also be empty.
hats = [1,0,0,1,0,0,0,0,1,0]

# prevents that two threads calculates the same result
calculating_lock = threading.Lock()

def solution(X):
    # last is maybe not correct and is still calculated in another Thread
    if(len(hats) > X):
        return hats[:X]
    # lock if no thread is calculating right now
    while not calculating_lock.acquire(False):
        sleep(0.1)
        # still locked but maybe the other thread did my work
        if(len(hats) > X):
            return hats[:X]
    for current_dwarf in range(len(hats),X+1):
        # init default
        hats.append(1)
        for ii in range(2,current_dwarf+2):
            if (current_dwarf + 1) % ii == 0:
                # using Bit Operations
                hats[current_dwarf] ^= 1
        # reset all other bits to 0
        hats[current_dwarf] &= 1
    calculating_lock.release()
    return hats[:X]
    pass
