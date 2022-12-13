import random
import time
from multiprocessing import Process, Value, Array, Queue, Pipe, Lock
import os
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sys


def main_fun(communicator:Queue, outputs, counter, l, end):
    time.sleep(1)
    l.acquire()
    data = communicator.get()
    print('inputs', data)

    if data == [True, True, False]:  # coming in
        outputs[0] = 0 # err = "off"
        outputs[1] = 1  # "on"
        outputs[2] = 1  # "on"
        outputs[3] = 1  # "on"
        counter.value += 1
    elif data == [True, True, True] and counter.value >= 1:  # coming in
        outputs[0] = 0 # err = "off"
        outputs[3] = 1   # "on"
        counter.value += 1
    elif data == [True, False, True] and counter.value - 1 > 0:  # coming out
        outputs[0] = 0 # err = "off"
        outputs[3] = 1
        counter.value -= 1
    elif data == [True, False, True] and counter.value - 1 == 0:  # coming out last one
        outputs[0] = 0 # err = "off"
        outputs[1] = 0
        outputs[2] = 0
        outputs[3] = 1
        counter.value -= 1
    elif data == [True, False, False] or data == [True, False, True] and counter.value - 1 < 0 or data == [True, True, True] and counter.value < 1:
        outputs[0] = 1  # err = "on"
        outputs[1] = 0
        outputs[2] = 0
        outputs[3] = 0
        end.value = 1

    print('outputs', outputs[:])
    print('Amount of people in house', counter.value)
    print()
    l.release()

    # visualization
    fig = plt.figure()
    names = ['Err', 'L', 'M', 'R']
    ax = plt.bar(names, outputs)
    plt.show()
    time.sleep(3)

def inputs(q, l): # getting inputs from sensors - door, in, out
    while True:
        l.acquire()
        q.put([random.choice([True, False]), random.choice([True, False]), random.choice([True, False])])  # Door,In,Out
        time.sleep(1)
        l.release()

if __name__ == '__main__':
    counter = Value('i', 0)
    outputs = Array('i', [0, 0, 0, 0])  # Err, L, M, R - all of them "off"
    end = Value('i', 0)

    l = Lock()
    q = Queue()
    p_queue = Process(target=inputs, args=(q, l))
    p_queue.start()

    time.sleep(2)
    while end.value == 0:
        main_fun(q, outputs, counter, l, end)

    p_queue.terminate()
    p_queue.join()
    if outputs[0] == 1: #exception
        raise RuntimeError("Error!")
