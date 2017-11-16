import cozmo
from cozmo.util import degrees, distance_inches, speed_mmps
from enum import Enum

DEGREES_PER_DIRECTION = 45

class nav_direction:

    def __init__(self, value, name):
        self.value = value
        self.name = name

class nav(nav_direction):
    North = nav_direction(0, "North")
    NorthEast = nav_direction(1, "NorthEast")
    East = nav_direction(2, "East")
    SouthEast = nav_direction(3, "SouthEast")
    South = nav_direction(4, "South")
    SouthWest = nav_direction(5, "SouthWest")
    West = nav_direction(6, "West")
    NorthWest = nav_direction(7, "NorthWest")

class cozmo_motion:

    def __init__(self):
        self.orientation = nav.North
        #self.robot = cozmo.robot.Robot

    def pointDirection(self, robot, next_point, current_point):

        # Get deltas
        dx = next_point.x - current_point.x
        dy = next_point.y - current_point.y

        # Determine direction of movement
        if (dx == 0 and dy == -1):
            new_orientation = nav.North
        elif (dx == 1 and dy == -1):
            new_orientation = nav.NorthEast
        elif (dx == 1 and dy == 0):
            new_orientation = nav.East
        elif (dx == 1 and dy == 1):
            new_orientation = nav.SouthEast
        elif (dx == 0 and dy == 1):
            new_orientation = nav.South
        elif (dx == -1 and dy == 1):
            new_orientation = nav.SouthWest
        elif (dx == -1 and dy == 0):
            new_orientation = nav.West
        else:
            new_orientation = nav.NorthWest

        # Find rotational angle
        print("    Direction: ", new_orientation.name)
        self.get_rotation_angle(robot, new_orientation)


    def get_rotation_angle(self, robot, target_orientation):
        
        # Calculate degrees to rotate
        degrees = (target_orientation.value - self.orientation.value ) * DEGREES_PER_DIRECTION

        # Always rotate the shortest amount necessary
        if degrees > 180:
            degrees -= 360
        if degrees < -180:
            degrees += 360

        degrees = degrees * -1
        print ("    Rotating {} degrees".format(degrees))

        # Set new orientation
        self.cozmo_program(robot, degrees)
        self.orientation = target_orientation


    # Cozmo functions
    def cozmo_program(self, robot, degree):
        if degree != 0 :
            print("Degree:", degree)
            robot.turn_in_place(degrees(degree)).wait_for_completed()
        robot.drive_straight(distance_inches(4), speed_mmps(50)).wait_for_completed()

    def goal_reached(self, robot):
        robot.say_text("Goal Reached").wait_for_completed()
        robot.say_text("I am the Best").wait_for_completed()