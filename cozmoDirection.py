import cozmo

from cozmo.util import degrees, distance_inches, speed_mmps
from enum import Enum

class direction(Enum):
    South = 0
    North = 1
    East = 2
    West = 3
    SouthEast = 4
    NorthEast = 5
    SouthWest = 6
    NorthWest = 7

class cozmo_motion:

    def __init__(self):
        self.DEGREE = 0

    def pointDirection(self, newpoint, oldpoint):
        dx = newpoint.x - oldpoint.x
        dy = newpoint.y - oldpoint.y
        if (dx == 0 and dy == 1):
            value = 0
        elif (dx == 0 and dy == 1):
            value = 1
        elif (dx == 1 and dy == 0):
            value =2
        elif (dx == -1 and dy == 0):
            value =3
        elif (dx == 1 and dy == 1):
            value = 4
        elif (dx == 1 and dy == -1):
            value = 5
        elif (dx == -1 and dy == 1):
            value = 6
        else:
            value = 7
        self.cozmoDirection(value)

    def cozmoDirection(self, direct):
        if direct == 0:
            self.DEGREE = self.DEGREE + 0
        elif direct == 1:
            self.DEGREE = self.DEGREE + 180
        elif direct == 2:
            self.DEGREE = self.DEGREE - 90
        elif direct == 3:
            self.DEGREE = self.DEGREE + 90
        elif direct == 4:
            self.DEGREE = self.DEGREE - 45
        elif direct == 5:
            self.DEGREE = self.DEGREE - 135
        elif direct == 6:
            self.DEGREE = self.DEGREE + 45
        else:
            self.DEGREE = self.DEGREE + 135
        print ("direction / degree", direct, self.DEGREE)
        #self.cozmo_program(cozmo.robot.Robot, self.DEGREE)

    def cozmo_program(robot: cozmo.robot.Robot, degree):
        if degree != 0 :
            robot.turn_in_place(degree).wait_for_completed()
        robot.drive_straight(distance_inches(4), speed_mmps(50)).wait_for_completed()

    def goal_reached(robot: cozmo.robot.Robot):
        robot.say_text("Goal Reached").wait_for_completed()
        robot.say_text("I am the Best").wait_for_completed()