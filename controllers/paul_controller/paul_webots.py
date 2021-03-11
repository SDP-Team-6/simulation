# API for Webots used to define Paul class
# Python 3

# Imports go here
from controller import Robot, Motor, DistanceSensor


# Paul class is used to define a set of standard function calls (an API) to define how the controller interacts
# with the environment (Webots, Hardware etc.)
class Paul(object):
    def __init__(self):
        # Name of the controller
        self.name = "PAUL controller for Webots"

        # Current Speed of the robot (Used for exception handling recovery)
        self.speed = 0
        self.up_speed = 5
        self.down_speed = -5

        # May want to consider making both of these final variables
        self.top_threshold = 1000
        self.bottom_threshold = 1000

        # create the Robot instance.
        self.robot = Robot()

        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        # initialise the 3 wheels
        self.wheels = []
        wheelsNames = ['wheel1', 'wheel2', 'wheel3']

        for i in range(3):
            self.wheels.append(self.robot.getDevice(wheelsNames[i]))
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)  # unit: rad/s

        # initialise distance sensors
        self.top_ds = self.robot.getDevice('ds_top')
        self.bottom_ds = self.robot.getDevice('ds_bottom')
        self.top_ds.enable(self.timestep)
        self.bottom_ds.enable(self.timestep)
        # initialise LED
        self.uv_led = self.robot.getDevice('uv_led')

        # In the case that at init both distance sensors were already within a threshold, don't start up
        self.completed_init = True

        if self.check_top_ds_reading() and self.check_bottom_ds_reading():
            self.completed_init = False

    # Movement Functions
    # Function to start the robot moving at a speed defined in the speed parameter
    def start_motors(self, speed):
        print("Starting motors...")
        self.speed = speed
        for i in range(3):
            self.wheels[i].setVelocity(speed)

    # Function to stop the robot moving
    def stop_motors(self):
        print("Stopping motors...")
        self.speed = 0
        for i in range(3):
            self.wheels[i].setVelocity(0)

    # Motors and Sensors Readings
    # Function to display all readings from the motors and sensors
    def display_all_readings(self):
        self.display_motor_readings()
        self.display_top_ds_reading()
        self.display_bottom_ds_reading()

    # Function to display any readings from the motors
    def display_motor_readings(self):
        print("Motor speed: " + str(self.speed))

    # Function get the current speed of the robot
    # TODO: Potentially remove, equivalent to getSpeed?
    def get_motor_readings(self):
        return self.speed

    # Function to check if the top distance sensor reading is within the threshold to trigger a change in direction
    # Returns True  if the distance should change
    # Returns False if the distance is not within the threshold
    def check_top_ds_reading(self):
        return self.get_top_ds_reading() < self.get_top_threshold()

    # Function to display any readings from the top distance sensor
    def display_top_ds_reading(self):
        print("Top DS Reading: " + str(self.get_top_ds_reading()))

    # Function to display get readings from the top distance sensor
    def get_top_ds_reading(self):
        return self.top_ds.getValue()

    # Function to check if the top distance sensor reading is within the threshold to trigger a change in direction
    # Returns True if the distance should change
    # Returns False if the distance is not within the threshold
    def check_bottom_ds_reading(self):
        return self.get_bottom_ds_reading() < self.get_bottom_threshold()

    # Function to display any readings from the bottom distance sensor
    def display_bottom_ds_reading(self):
        print("Bottom DS Reading: " + str(self.get_bottom_ds_reading()))

    # Function to display get readings from the bottom distance sensor
    def get_bottom_ds_reading(self):
        return self.bottom_ds.getValue()

    def turn_uv_on(self):
        self.uv_led.set(255)

    def turn_uv_off(self):
        self.uv_led.set(0)

    def wait_for_time(self, time):
        self.robot.waitForUserInputEvent(self.robot.EVENT_NO_EVENT, time)

    # Getters and Setters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_up_speed(self):
        return self.up_speed

    def set_up_speed(self, up_speed):
        self.up_speed = up_speed

    def get_down_speed(self):
        return self.down_speed

    def set_down_speed(self, down_speed):
        self.down_speed = down_speed

    def get_top_threshold(self):
        return self.top_threshold

    def set_top_threshold(self, top_threshold):
        self.top_threshold = top_threshold

    def get_bottom_threshold(self):
        return self.bottom_threshold

    def set_bottom_threshold(self, bottom_threshold):
        self.bottom_threshold = bottom_threshold