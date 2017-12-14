import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps
from cozmo.exceptions import RobotBusy
from time import sleep
import robot_vision as vision

angle_left = 5
angle_right = -5

kick_cycles = 10

wheel_speed = 1000
wheel_accl = 1000

class kicker():

    def __init__(self, parent):
        self.parent = parent
        self.kicking = False
        self.kick_time = 0
        print("Kicker Ready")

    # Handle new images
    def on_new_image(self, event, *, image:cozmo.world.CameraImage, **kw):

        # Look for a ball in the field of view
        
        # Experimental Code
        #ball = vision.detect_circle(image)

        # Nicks code
        ball = vision.detect_object(image)

        # Check that the right behavior is enabled
        if self.parent.behavior < 3:

            #try:
            #    self.parent.robot.set_lift_height(1, 10, 10, 2)
            #except RobotBusy:
            #    pass
            if self.kicking:
                self.kick()

            elif ball is not None:

                x_position = ball[0]

                # Line up with the ball if we aren't kicking yet
                if not self.kicking:
                    if x_position <= vision.left_of_screen_small:
                        try:
                            print("Driving left, X: {}".format(x_position))
                            self.parent.robot.turn_in_place(degrees(angle_left))
                        except RobotBusy:
                            pass
                    # If ball is in the middle of image
                    elif x_position >= vision.right_of_screen_small:
                        try:
                            print("Driving right, X: {}".format(x_position))
                            self.parent.robot.turn_in_place(degrees(angle_right))
                        except RobotBusy:
                            pass
                
                    else:
                        self.kick()
                else:
                    self.kick()

    # Execute the kick
    def kick(self):

        self.kicking = True

        if self.kick_time < kick_cycles:
            print("Kicking")

            # Drive at ball
            self.parent.robot.drive_wheel_motors(
                            wheel_speed,
                            wheel_speed,
                            wheel_accl,
                            wheel_accl)

        else:
            print("Stopping")
            self.parent.robot.stop_all_motors()

        # INcriment kick time
        self.kick_time += 1
