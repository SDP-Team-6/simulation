# Controller for robot used to call correct functions from corresponding API
# Python 2/3 (Should work with both versions but check requirements of API/ required libraries)

# Import the API that should be used by the controller
# Syntax: from <api_file_name> import paul
from paul_webots import Paul

# Import time library
from time import time, sleep

# Determine if we are currently working on hardware or sim
hardware = False

# Starting time of the robot (in seconds from epoch)
start_time = time()

# Instance of Paul class
paul = Paul()

# Time step (in seconds)
# Use a sleep of at least 0.1, to avoid errors (This applies to Hardware implementations)
time_step = 0.2

# Max run time of the robot before termination (in seconds)
run_time = 20

# Used to stop the robot before the time is finished
running = True

# Used to toggle displaying the readings from sensors and motors
display = False

# stores current direction & state
going_up = True

# stores uv disinfection state
uv_on = True

# Start the initial movement of the robot
paul.start_motors(paul.get_up_speed())
paul.turn_uv_on()

# THIS WAS THE LINE PREVIOUS BUT FOR WHATEVER REASON IT CRASHES IF I USE IT
# WEBOTS GETS ANGRY ABOUT RETURNING BUT UNCLEAR ON HOW TO FIX
# while running and time() < start_time + run_time:

while paul.robot.step(paul.timestep) != -1:
    try:
        # If the display option is enabled display all readings as defined in the API
        if display:
            paul.display_all_readings()

        # If the robot is moving up the pole
        if going_up:
            # Check that the robot has gone past the distance sensor stopping threshold
            if paul.check_top_ds_reading():
                # If the robot has reached the ceiling the move the robot down
                going_up = False
                paul.stop_motors()
                paul.start_motors(paul.get_down_speed())

        # If the robot is moving down the pole
        elif not going_up:
            if paul.check_bottom_ds_reading():
                # If the robot has reached the floor then move the robot back up
                going_up = True
                paul.stop_motors()
                paul.start_motors(paul.get_up_speed())
        else:
            # If there the robot is not moving up or down then there is an issue and the code should be
            # terminated
            paul.stop_motors()
            paul.turn_uv_off()

        # Pause the program for a set duration, not required on the simulation version
        if hardware:
            sleep(time_step)

    # Catch any exceptions that occur during execution
    # these may affect the motors and lead to an unexpected termination of the loop
    # A I/O error can occur during while using the Raspberry Pi API (This is unavoidable and should be handled.

    except Exception as e:
        pass
        # Note: Below print statement will only work in Python2
        # print str(e)
        # Stop and restart the motors if an error occurs
        paul.stop_motors()
        paul.turn_uv_off()
        print("Error")
        paul.display_all_readings()

        # I've just put 5 here for now, getting the speed won't work because it has just been stopped
        # TODO: Figure out we want to do here
        paul.start_motors(5)