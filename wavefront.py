import csv
import sys

CONST_BEGIN = -2
CONST_GOAL = -3

class point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def printable(self):
        string = "x:{}, y:{}".format(self.x, self.y)
        return string

class map_object(point):

    def __init__(self):
        self.vector = []
        self.width = 0
        self.height = 0

    def in_map(self, point):
        try:
            if point.x < 0 or point.x >= self.width:
                return False
            if point.y < 0 or point.y >= self.height:
                return False
            return True

        # If this fails for any reason the point is not in the map
        except:
            return False


# Read in map from map.csv file
map = map_object()
with open("map.csv") as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        int_row = [ int(value) for value in row]
        map.vector.append(int_row)

# Set map size
map.width = len(map.vector[0])
map.height = len(map.vector)

# Print dimetions
print("Map Dimentions: {}x{}".format(map.width, map.height))

# Find start and goal positions
# 2 = start
# 3 = end
# 0 = open space
# 1 = obstruction
start_defined = False
goal_defined = False
for x in range(0, map.width):
    for y in range(0, map.height):
    
        if map.vector[y][x] == CONST_BEGIN:
            start = point(y, x)
            start_defined = True

        if map.vector[y][x] == CONST_GOAL:
            goal = point(y, x)
            goal_defined = True

# Check for initialization of start and goal positions
if (start_defined and goal_defined):
    print("Problem defined, start: {}, goal: {}".format(start, goal))
else:
    print("Problem undefined")
    sys.exit()

# Run wavefront algorithm - 8 connected
print("Start: ", start.printable())
for x in range(start.x - 1, start.x + 2):
    for y in range(start.y - 1, start.y + 2):

        # Move to the new point
        new_point = point(x, y)
        if not map.in_map(new_point):
            print("Point not in map: ", new_point.printable())
        else:
            print("Moving to point: ", new_point.printable())


print("Done")