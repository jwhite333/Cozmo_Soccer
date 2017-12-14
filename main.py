# Beginning of module to handle transitions between states

import cozmo
from block_events import poll_events
from goal_tend import keeper
from kick import kicker
from time import sleep

# Behaviors
# 0 - Stop
# 1 - Primary behavior
# 2 - Secondary behavior
# 3 - Stop

class penalty_kick():

    def __init__(self, robot):
        self.poll_thread = poll_events(self)
        self.behavior = 0
        self.robot = robot

        # Initialize camera
        self.robot.camera.image_stream_enabled
        self.robot.set_head_light(True)
        self.robot.camera.color_image_enabled = True
        action = self.robot.set_lift_height(0)
        action.wait_for_completed()
        action = self.robot.set_head_angle(cozmo.util.Angle(degrees=-10))
        action.wait_for_completed()
        #sleep(1)

        # Initialize behavior, change to update position
        #self.player = keeper(self)
        self.player = kicker(self)
        self.robot.add_event_handler(cozmo.world.EvtNewCameraImage, self.player.on_new_image)

    # Begin execution
    def start(self):
        print("Starting Execution")
        self.poll_thread.start()

    # Stop execution
    def stop(self):
        self.poll_thread.join()
        print("Stopping...")


# Create state machine instance
def main(robot: cozmo.robot.Robot):

    pk = penalty_kick(robot)
    pk.start()
    pk.stop()

# Start program
cozmo.run_program(main, use_viewer=True) # , use_viewer=True, force_viewer_on_top=True


