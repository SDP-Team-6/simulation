from controller import Motor
from controller import Robot
from controller import Device

#  This can be useful for debugging, it lists
#  All of the devices currently connected to the robot
#  by their name.

# for i in range(robot.getNumberOfDevices()):
    # tag = robot.getDeviceByIndex(i)
    
    
    # print(Device.getName(tag))

TIME_STEP = 64
robot = Robot()


wheels = []
wheelsNames = ['wheel1', 'wheel2'] 
for i in range(2):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

ds = []
dsNames = ['dis_sensor']
ds.append(robot.getDevice(dsNames[0]))
ds[0].enable(TIME_STEP)
avoidObstacleCounter = 0

while robot.step(TIME_STEP) != -1:

    climbSpeed = -10.0
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        climbSpeed = 10.0
    else:
        if ds[0].getValue() < 950.0:
            avoidObstacleCounter = 50 # change this value to make the
                                      # robot move up and down in 
                                      # specific length
    wheels[0].setVelocity(climbSpeed)
    wheels[1].setVelocity(climbSpeed)