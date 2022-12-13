from random import randint
from StateMachine import StateMachine

# states time cycles
cool = 2+1
heat = 3+1

def coolOn (pov):

    if (pov[0] > 0):
        pov[0] = pov[0] - 1

    input = randint(10, 30)
    output = None

    print ("c: ", pov[0])
    print("Temp is: ", input)

    if (input < 20 and pov[0] == 0):# the temperature is too low and the clock finished --> move to coolOff state
        newState = "coolOff"
        pov[0] = cool

    else:
        newState = "coolOn"

    print ("new state: ", newState)
    return newState, pov, output

def coolOff (pov):

    if (pov[0] > 0):
        pov[0] = pov[0] - 1

    input = randint(10,30)
    output = None

    print("c: ", pov[0])
    print("Temp is: ", input)

    if pov[1] == 0:
        newState = "End_state"

    else:
        if (input > 20 and pov[0] == 0): # the temperature is too high and the clock finished --> move to coolOn state
            newState = "coolOn"
            output = "coolOn"
            pov[0] = heat
            pov[1] = pov[1] - 1 # we finished another cycle


        else:
            newState = "coolOff"

    print ("new state: ", newState)
    return newState, pov, output

def end_state(txt):
    print("Time to go")
    return "End_State", ""

if __name__ == '__main__':
    m = StateMachine()
    m.add_state("coolOff", coolOff)
    m.add_state("coolOn", coolOn)
    m.add_state("End_state", end_state, end_state=1)

    m.set_start("coolOff")

    print("Initial state: coolOff")
    pov = [cool, 2]
    m.run(pov, 0.1)
