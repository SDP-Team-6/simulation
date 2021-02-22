# Controller for robot used to call correct functions from corresponding API
# Python 2/3 (Should work with both versions but check requirements of API/ required libraries)

# Import the API that should be used by the controller
# Syntax: from <api_file_name> import paul
from paul_skeleton import Paul

# Import time library
from time import time, sleep

# Instance of Paul class
paul = Paul()

# Time step (in seconds)
# Use a sleep of at least 0.1, to avoid errors (This applies to Hardware implementations)
time_step = 0.2
# Max run time of the robot before termination (in seconds)
run_time = 10

# Used to stop the robot before the time is finished
running = True

# Used to toggle displaying the readings from sensors and motors
display = False

# stores current direction & state
going_up = True

# Starting time of the robot (in seconds from epoch)
start_time = time()

# Start the robot moving up the pole
paul.start_motors(paul.get_up_speed())

# Keep running the robot until it should stop or exceeds the run time
while running and time() < start_time + run_time:
    try:
        # If the display option is enabled display all readings as defined in the API
        if display:
            paul.display_all_readings()

        # If the robot is moving up the pole
        if going_up:
            # Check that the robot has gone past the distance sensor stopping threshold
            if paul.check_top_ds_reading():
                # If the robot has reached the ceiling the move the robot down
                goingUp = False
                paul.stop_motors()
                paul.start_motors(paul.get_down_speed())

        # If the robot is moving down the pole
        elif not going_up:
            if paul.check_bottom_ds_reading():
                # If the robot has reached the floor then move the robot back up
                goingUp = True
                paul.stop_motors()
                paul.start_motors(paul.get_up_speed())
        else:
            # If there the robot is not moving up or down then there is an issue and the code should be terminated
            paul.stop_motors()
            running = False

        # Pause the program for a set duration
        sleep(time_step)

    # Catch any exceptions that occure during execution
    # these may affect the motors and lead to an unexpected termination of the loop
    # A I/O error can occur during while using the Raspberry Pi API (This is unavoidable and should be handled)
    except Exception as e:
        # Note: Below print statement will only work in Python2
        # print str(e)
        # Stop and restart the motors if an error occurs
        paul.stop_motors()
        paul.start_motors(paul.get_speed())

# Tidy up - code to be executed before the script terminates
paul.stop_motors()