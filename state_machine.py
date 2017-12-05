# Beginning of module to handle transitions between states

#from threading import Thread
import queue
import cozmo

from block_events import poll_events
from goal_tend import keeper
from kick import kicker

class state_machine():

    def __init__(self, robot):
        self.message_queue = queue.Queue()
        self.running = False
        self.robot = robot
        self.poll_thread = poll_events(self)

        # Initialize behavior thread, change to update position
        self.player_thread = keeper(self)

    # Begin execution
    def start(self):
        print("Starting Execution")
        self.running = True
        self.poll_thread.start()
        self.player_thread.start()

    # Stop execution
    def stop(self):
        self.poll_thread.join()
        self.player_thread.join()





# Create state machine instance
def main(robot: cozmo.robot.Robot):

    SM = state_machine(robot)
    SM.start()
    SM.stop()

# Start program
cozmo.run_program(main)


