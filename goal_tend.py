import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.exceptions import RobotBusy
from time import sleep
import robot_vision as vision

turn_speed = 100
wheel_speed = 200

movement_distance = 5

class keeper(): # Thread

    def __init__(self, parent):
        self.parent = parent
        self.ball_initial_location = None
        self.kicked = False
        print("Initializing keeper")

    # Handle new images
    def on_new_image(self, event, *, image:cozmo.world.CameraImage, **kw):

        # Look for a ball in the field of view
        
        # Experimental Code
        # ball = vision.detect_circle(image)

        # Nicks code
        ball = vision.detect_object(image)

        # Turn so that the circle is on the left of our field of view
        if self.parent.behavior < 3:

            if ball is not None:

                x = ball[0]

                # Check if ball has been moved
                if self.ball_initial_location is not None:
                    distance_moved = self.ball_initial_location - x

                    if abs(distance_moved) > movement_distance:
                        self.kicked = True
                else:
                    self.ball_initial_location = x

                if self.kicked:

                    # Drive
                    self.move_to_ball(x)
                    
            else:
                self.parent.robot.stop_all_motors()

        else:
            self.parent.robot.stop_all_motors()


    # Drive towards the ball
    def move_to_ball(self, ball_x_val):

        # If ball is to the left of image
        print("x: {}".format(ball_x_val))
        if ball_x_val < vision.left_of_screen_small:
            print("Driving left, X: {}".format(ball_x_val))
            self.parent.robot.drive_wheel_motors(
                            wheel_speed - turn_speed,
                            wheel_speed)
        # If ball is in the middle of image
        elif ball_x_val > vision.right_of_screen_small:
            print("Driving right, X: {}".format(ball_x_val))
            self.parent.robot.drive_wheel_motors(
                            wheel_speed,
                            wheel_speed - turn_speed)
        # If ball is to the right of image
        else:                
            print("Driving straight, X: {}".format(ball_x_val))
            self.parent.robot.drive_wheel_motors(
                            wheel_speed,
                            wheel_speed)

