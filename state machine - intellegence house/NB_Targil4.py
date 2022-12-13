import random
from random import randint
from StateMachine import StateMachine
import time

# robot movement time

Trsh_Robot = 2


def entrance(pov):
    time.sleep(Trsh_Robot)
    newState = 'wait'
    outputs['R'] = 'Off'
    print("new state: ", newState)
    return newState, pov, ''


def exit(pov):
    time.sleep(Trsh_Robot)
    newState = 'wait'
    outputs['R'] = 'Off'
    print("new state: ", newState)
    return newState, pov, ''


def wait(pov):
    random_temp = random.randint(0, 3)
    if pov:
        random_temp = 1
        pov = False
    print('random input:', (list(inputs.keys())[list(inputs.values()).index(random_temp)]))
    if random_temp == 0:  # entrance and exit at the same time:
        newState = 'entrance'
        outputs['Count'] += 1
        outputs['R'] = 'On'
        outputs['L'] = 'On'
        outputs['M'] = 'On'
        pov = True  # there is a person waiting to get out
    if random_temp == 1:  # exit
        if outputs['Count'] - 1 > 0:  # exit and there still people inside
            newState = 'exit'
            outputs['Count'] -= 1
            outputs['R'] = 'On'
        elif outputs['Count'] - 1 == 0:  # exit and no one left inside
            newState = 'exit'
            outputs['Count'] -= 1
            outputs['L'] = 'Off'
            outputs['M'] = 'Off'
            outputs['R'] = 'On'
        else:  # error count -1 <0 - exit and the house is empty
            newState = 'Error'
            outputs['Err'] = 'On'
            print('Error! The house is empty, can not be out input')

    if random_temp == 2:  # entrance only
        newState = 'entrance'
        outputs['Count'] += 1
        outputs['L'] = 'On'
        outputs['M'] = 'On'
        outputs['R'] = 'On'
    if random_temp == 3:  # entrance only
        newState = 'Error'
        outputs['Err'] = 'On'
        print('Error! The door can not be open without in or out')

    print("new state: ", newState)
    print("outputs: ", outputs)

    return newState, outputs, ''


def error(pov):
    return "End_State", ""


if __name__ == '__main__':
    m = StateMachine()

    # states of the machine
    m.add_state("entrance", entrance)
    m.add_state("exit", exit)
    m.add_state("wait", wait)
    m.add_state("error", error, end_state=1)

    # initial state
    m.set_start("wait")

    # initial inputs and outputs for system

    print("Initial state: wait")
    inputs = {'Door Out In': 0,
              'Door Out notIn': 1,
              'Door In notOut': 2,
              'Door notIn notOut': 3}

    outputs = {'Count': 0, 'L': 'Off', 'M': 'Off', 'R': 'Off', 'Err': 'Off'}
    pov = False
    m.run(pov)
