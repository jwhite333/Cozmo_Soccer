import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps
from cozmo.exceptions import RobotBusy
from time import sleep
import robot_vision as vision

turn_right = -5
turn_left = 5

kick_phase_1 = 15
kick_phase_2 = 18

wheel_speed = 400
turn_speed = 400

class kicker():

    def __init__(self, parent):
        self.parent = parent
        self.kicking = False
        self.kick_time = 0
        print("Initializing kicker")

    # Handle new images
    def on_new_image(self, event, *, image:cozmo.world.CameraImage, **kw):

        # Look for a ball in the field of view
        
        # Experimental Code
        #ball = vision.detect_circle(image)

        # Nicks code
        ball = vision.detect_object(image)

        if self.parent.behavior < 3:
            
            if ball is not None:

                ball_x_val = ball[0]

                if not self.kicking:
                    if ball_x_val <= vision.left_of_screen_wide:
                        try:
                            print("Driving left, X: {}".format(ball_x_val))
                            self.parent.robot.turn_in_place(degrees(turn_left))
                        except RobotBusy:
                            pass
                    # If ball is in the middle of image
                    elif ball_x_val >= vision.right_of_screen_wide:
                        try:
                            print("Driving right, X: {}".format(ball_x_val))
                            self.parent.robot.turn_in_place(degrees(turn_right))
                        except RobotBusy:
                            pass
                
                    else:
                        self.kick()
                else:
                    self.kick()
                
    def kick(self):

        self.kicking = True

        if self.kick_time < kick_phase_1:
            print("Kicking")

            # Drive at ball
            self.parent.robot.drive_wheel_motors(
                            wheel_speed,
                            wheel_speed)

            self.kick_time += 1

        elif self.kick_time < kick_phase_2:
            print("Kicking and turning")

            # Drive at ball
            self.parent.robot.drive_wheel_motors(
                                wheel_speed,
                                wheel_speed - turn_speed)

            self.kick_time += 1

        else:
            print("Stopping")
            self.parent.robot.stop_all_motors()
            

            

            