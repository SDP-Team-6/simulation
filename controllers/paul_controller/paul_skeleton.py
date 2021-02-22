# API for <insert_description> used to define Paul class
# Python 2/3

# Imports go here

from controller import Robot, Motor, DistanceSensor


# Paul class is used to define a set of standard function calls (an API) to define how the controller interacts
# with the enviroment (Webots, Hardware etc.)
class Paul(object):
    def __init__(self):

        # Name of the controller
        self.name = "PAUL Webots"
        # Create the robot instance in the simulation
        # IT CRASHES ON THE LINE BELOW, UNSURE WHY AT THE MOMENT, PRETTY SURE IT'S GOT SOMETHING
        # TO DO WITH THE CONTROLLER IMPORT BUT NOT ENTIRELY SURE HOW IT WORKS ATM
        self.paul = Robot()

        # Current Speed of the robot (Used for exception handling recovery)
        self.speed = None
        # Speed that the robot will travel up
        # TODO Figure out how this value relates to real world
        self.up_speed = 5
        # Speed that the robot will travel down
        # TODO Figure out how this value relates to real world
        self.down_speed = 5
        print("Test3")

        # TODO Consider if these should be final variables
        # Threshold reading on top distance sensors before triggering
        self.top_threshold = 1000
        # Threshold reading on  distance sensors before triggering
        self.bottom_threshold = 1000

        print("Test4")
        # Note: The following should only be set if distance sensors are not attached
        # they should be set to 0 if sensors are attached.
        # Reading value from the top distance sensor
        self.top_ds_reading = None
        # Reading value from the bottom distance sensor
        self.bottom_ds_reading = None

        print("Test5")

        # I need to define this here in order to define the sampling period
        # for the distance sensors
        self.timestep = int(self.paul.getBasicTimeStep())

        # Set up all of the devices that the robot will need to use
        wheel_names = ['wheel1', 'wheel2', 'wheel3']
        distance_sensor_names = ['ds_top', 'ds_bottom']

        self.wheels = []
        self.distance_sensors = []

        for i in range(0, len(wheel_names)):
            self.wheels.append(self.paul.getDevice(wheel_names[i]))
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)  # Measured in rad/s

        # Decided to set it up like this to allow us to add additional distance sensors
        # to ensure that all points of the robot are at the same distance from the top / bottom
        for i in range(0, len(distance_sensor_names)):
            self.distance_sensors.append(self.paul.getDevice(distance_sensor_names[i]))
            self.distance_sensors[i].enable(self.timestep)

        self.uv_lights = self.paul.getDevice('uv_led')
        print("Test5")

    # Movement Functions
    # Function to start the robot moving at a speed defined in the speed parameter
    def start_motors(self, speed):
        print('Starting motors...')
        self.__set_wheel_speed(speed)

    # Function to stop the robot moving
    def stop_motors(self):
        print('Stopping motors...')
        self.__set_wheel_speed(0)

    # Motors and Sensors Readings
    # Function to display all readings from the motors and sensors
    # If not required then dont add any code
    def display_all_readings(self):
        self.display_motor_readings()
        self.display_top_ds_reading()
        self.display_bottom_ds_reading()

    # Function to display any readings from the motors
    # Note: Not essential - can be left unchanged if not needed
    def display_motor_readings(self):
        print("Motor readings: " + str(self.speed))

    # Function get the current speed of the robot
    def get_motor_readings(self):
        return self.speed

    # Function to check if the top distance sensor reading is within the threshold to trigger a change in direction
    # Returns True if the distance should change
    # Returns False if the distance is not within the threshold
    def check_top_ds_reading(self):
        return self.paul.get_top_ds_reading() < self.paul.get_top_threshold()

    # Function to display any readings from the top distance sensor
    # Note: Not essential - can be left unchanged if not needed
    def display_top_ds_reading(self):
        print("Top DS Reading: " + str(self.top_ds_reading))

    # Function to display get readings from the top distance sensor
    def get_top_ds_reading(self):
        self.top_ds_reading = self.distance_sensors[0].getValue()
        return self.top_ds_reading

    # Function to check if the top distance sensor reading is within the threshold to trigger a change in direction
    # Returns True if the distance should change
    # Returns False if the distance is not within the threshold
    def check_bottom_ds_reading(self):
        return self.paul.get_bottom_ds_reading() < self.paul.get_bottom_threshold()

    # Function to display any readings from the bottom distance sensor
    # Note: Not essential - can be left unchanged if not needed
    def display_bottom_ds_reading(self):
        print("Bottom DS Reading: " + str(self.bottom_ds_reading))

    # Function to display get readings from the bottom distance sensor
    def get_bottom_ds_reading(self):
        self.bottom_ds_reading = self.distance_sensors[1].getValue()
        return self.bottom_ds_reading

    # Private function to set the speed of the wheels used as a helper function
    def __set_wheel_speed(self, speed):
        self.speed = speed
        for i in self.wheels:
            i.setVelocity(speed)

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

    def set_down_speed(self, up_speed):
        self.down_speed = up_speed

    def get_top_threshold(self):
        return self.top_threshold

    def set_top_threshold(self, top_threshold):
        self.top_threshold = top_threshold

    def get_bottom_threshold(self):
        return self.bottom_threshold

    def set_bottom_threshold(self, bottom_threshold):
        self.bottom_threshold = bottom_threshold
