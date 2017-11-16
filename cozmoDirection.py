import cozmo

from cozmo.util import DEGREEs, distance_inches, speed_mmps
from enum import Enum

DEGREE = 0

class direction(Enum):
    North = 0
    South = 1
    East = 2
    West = 3
    NorthEast = 4
    SouthEast = 5
    NorthWest = 6
    SouthWest = 7

def poitnDirection(newpoint, oldpoint):
    dx = newpoint.x - oldpoint.x
    dy = newpoint.y - oldpoint.y
    if (dx == 0 and dy == 1):
        value = 0
        cozmoDirection(value)
    elif (dx == 0 and dy == 1):
        value = 1
        cozmoDirection(value)
    elif (dx == 1 and dy == 0):
        value =2
        cozmoDirection(value)
    elif (dx == -1 and dy == 0):
        value =3
        cozmoDirection(value)
    elif (dx == 1 and dy == 1):
        value = 4
        cozmoDirection(value)
    elif (dx == 1 and dy == -1):
        value = 5
        cozmoDirection(value)
    elif (dx == -1 and dy == 1):
        value = 6
        cozmoDirection(value)
    else:
        value = 7
        cozmoDirection(value)

def cozmoDirection(direct):
    if direct == 0:
        DEGREE = DEGREE + 0
    elif direct == 1:
        DEGREE = DEGREE + 180
    elif direct == 2:
        DEGREE = DEGREE - 90
    elif direct == 3:
        DEGREE = DEGREE + 90
    elif direct == 4:
        DEGREE = DEGREE - 45
    elif direct == 5:
        DEGREE = DEGREE - 135
    elif direct == 6:
        DEGREE = DEGREE + 45
    else:
        DEGREE = DEGREE + 135
    cozmo_program(cozmo.robot.Robot, DEGREE)

def cozmo_program(robot: cozmo.robot.Robot, DEGREE):
    if DEGREE != 0 :
        robot.turn_in_place(DEGREEs(DEGREE)).wait_for_completed()
    robot.drive_straight(distance_inches(4), speed_mmps(50)).wait_for_completed()

def goal_reached(robot: cozmo.robot.Robot):
    robot.say_text("Goal Reached").wait_for_completed()
    robot.say_text("I am the Best").wait_for_completed()

