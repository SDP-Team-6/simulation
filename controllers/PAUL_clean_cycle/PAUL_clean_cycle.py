"""PAUL_demo1 controller."""

from controller import Robot, Motor, DistanceSensor

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# initialise the 3 wheels
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3']
for i in range(3):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0) # unit: rad/s
# initialise distance sensors
ds_top = robot.getDevice('ds_top')
ds_bottom = robot.getDevice('ds_bottom')
ds_top.enable(timestep)
ds_bottom.enable(timestep)
# initialise LED
uv_led = robot.getDevice('uv_led')

# stores current direction & state
goingUp = True
# changingDir = False

def setSpeed(v):
    for i in range(3):
        wheels[i].setVelocity(v)

# number of tours for each cleaning cycle
# 1 tour up/down the pole = bottom -> top -> bottom
tours_in_each_cycle = 2
# count number of tours completed
count = 0
# pause time between cycles (milliseconds)
pause_time = 3000


# perform simulation steps until
# Webots is stopping the controller
while robot.step(timestep) != -1:


    # count number of tours completed
    #count = 0
    # one clean cycle
    #while count < tours_in_each_cycle:
        # if going up
    if goingUp:
        # turn on UV LED
        uv_led.set(255)
        if ds_top.getValue() < 1000:
            # reaching ceiling, stop
            goingUp = False
            setSpeed(0.0)
        else:
            # otherwise go up
            setSpeed(5)

    # if going down
    elif not goingUp:
        # turn on UV LED
        uv_led.set(0)
        if ds_bottom.getValue() < 1000:
            # reaching floor, stop
            goingUp = True
            setSpeed(0.0)
            # reached bottom -> current tour finished
            count += 1
            if count == tours_in_each_cycle:
                # pause a specified time between clean cycles
                robot.waitForUserInputEvent(robot.EVENT_NO_EVENT, pause_time)
                # clear count
                count = 0
        else:
            # otherwise go down
            setSpeed(-5)

    else:
        setSpeed(0.0)

# cleanup code if any
