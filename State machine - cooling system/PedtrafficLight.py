from random import randint
from StateMachine import StateMachine


# Cycle lengths
RedCycle = 60
YellowCycle = 5
GreenCycle = 60

# Red state handler
def red2green(poV):
    #print("red")
    poV[0] = poV[0] - 1
    tline = None
    if poV[1] == 0:
        newState = "End_state"
    else:
        if poV[0] == 0:
            newState = "Green"
            tline = "sigG"
            poV[0] = GreenCycle
            poV[1] = poV[1] - 1
        else:
            newState = "Red"
    return newState, poV, tline


# Green state handler
def green2yellow(poV):
    #print("green")
    if poV[0] > 0:
        poV[0] = poV[0] - 1
    tline = None
    pedestrian = randint(0, 40)
    if (pedestrian==0):
        print("pedestrian is here", "wait:",poV[0])
        if poV[0] == 0:
            newState = "Yellow"
            tline = "sigY"
            poV[0] = YellowCycle
        else:
            newState = "Pending"
    else:
        newState = "Green"
    return newState, poV, tline

# Pending state handler
def pending2yellow(poV):
    #print("pending")
    poV[0] = poV[0] - 1
    tline = None
    if poV[0] == 0:
        newState = "Yellow"
        tline = "sigY"
        poV[0] = YellowCycle
    else:
        newState = "Pending"
    return newState, poV, tline


# yellow state handler
def yellow2red(poV):
    #print("yellow")
    poV[0] = poV[0] - 1
    tline = None
    if poV[0] == 0:
        newState = "Red"
        tline = "sigR"
        poV[0] = RedCycle
    else:
        newState = "Yellow"
    return newState, poV, tline


def end_state(txt):
    print("Time to go")
    return "End_State", ""


if __name__ == '__main__':
    m = StateMachine()
    m.add_state("Red", red2green)
    m.add_state("Green", green2yellow)
    m.add_state("Pending", pending2yellow)
    m.add_state("Yellow", yellow2red)
    m.add_state("End_state", end_state, end_state=1)
    m.set_start("Red")


    print("sigR")
    po = [RedCycle, 5]
    m.run(po, 0.1)

