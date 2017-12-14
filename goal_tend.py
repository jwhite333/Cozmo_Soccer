import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.exceptions import RobotBusy
from time import sleep
import robot_vision as vision

wheel_speed = 300               # Max wheel speed
movement_distance = 7           # Distance ball needs to move before kicked=True
no_ball_stop_cycles = 20        # Abort behavior after not seeing the ball for this many cycles
target_location_left = 75       # X location to target if the ball was kicked right
target_location_right = 225     # X location to target if the ball was kicked left

class keeper(): # Thread

    def __init__(self, parent):
        self.parent = parent
        self.ball_initial_location = None
        self.ball_last_location = vision.screen_mid # Initialize to center of screen
        self.kicked = False
        self.no_ball_cycles = 0
        self.kick_left = False # False = left, True = right

        # PID Values
        self.speed_scalar = 0.9

        print("Keeper Ready")

    # Handle new images
    def on_new_image(self, event, *, image:cozmo.world.CameraImage, **kw):

        # Look for a ball in the field of view
        
        # Experimental Code
        #ball = vision.detect_circle(image)

        # Nicks code
        ball = vision.detect_object(image)

        # Check that the right behavior is enabled
        if self.parent.behavior < 3:
            if ball is not None:

                x_position = ball[0]
                self.no_ball_cycles = 0

                # Check if ball has been moved
                if self.ball_initial_location is not None:
                    distance_moved = self.ball_initial_location - x_position

                    # If ball has moved, set movement flag
                    if abs(distance_moved) > movement_distance and not self.kicked:
                        self.kicked = True
                        if distance_moved > 0:
                            self.kick_left = True

                elif not self.kicked:
                    self.ball_initial_location = x_position

                # If the ball has been kicked
                if self.kicked:

                    # I
                    integral_error = x_position - target_location_right if self.kick_left else x_position - target_location_left

                    # D
                    derivative = x_position - self.ball_last_location

                    # P
                    turn_severity = self.speed_scalar * (integral_error + derivative)

                    # Keep turn severity in range
                    if turn_severity < -wheel_speed:
                        turn_severity = -wheel_speed
                    if turn_severity > wheel_speed:
                        turn_severity = wheel_speed

                    # Drive
                    print("X: {:06.2f}, P: {:06.2f}, I: {:06.2f}, D: {:06.2f}, kick left: {}".format(
                        x_position,
                        turn_severity,
                        integral_error,
                        derivative,
                        self.kick_left
                    ))
                    self.move_to_ball(turn_severity)

                    # Set last position
                    self.ball_last_location = x_position
                    
            # If the ball is not seen stop
            else:

                if self.kicked:
                    self.no_ball_cycles += 1

                if self.no_ball_cycles >= no_ball_stop_cycles:
                    print("Havn't seen the ball in {} cycles, stopping...".format(no_ball_stop_cycles))
                    self.parent.robot.stop_all_motors()
                    self.parent.behavior = 3 # Stop

        # If the behavior is not the "on" behavior stop
        else:
            self.parent.robot.stop_all_motors()


    # Drive towards the ball
    def move_to_ball(self, turn_severity):

        # Adjust wheels acoording to turn severity
        self.parent.robot.drive_wheel_motors(
                            wheel_speed + turn_severity,
                            wheel_speed - turn_severity,
        )
        print("Normal")

