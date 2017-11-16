import csv
import sys

CONST_FREE_SPACE = 0
CONST_OBSTACLE = -1
CONST_START = -2
CONST_GOAL = -3

class tree_node:

    def __init__(self, value, address, parent, adjacency_list):
        self.value = value
        self.address = address
        self.parent = parent
        self.adjacency_list = adjacency_list
        self.visited = False

class point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def printable(self):
        string = "x:{}, y:{}".format(self.x, self.y)
        return string

    # d = get_direction(current_point, next_point)
    # d[0] = dx
    # d[1] = dy
    def get_direction(self, point):
        dx = point.x - self.x
        dy = point.y - self.y
        return dx, dy


class map_object(point):

    def __init__(self):
        self.map_2D = []
        self.graph = []
        self.start = None
        self.goal = None
        self.path = None
        self.eight_connected = True
    
    def free_map_2D(self):
        del self.map_2D[:]
        del self.map_2D

    def in_graph(self, point):
        try:
            if point.x < 0 or point.x >= len(self.graph[0]):
                return False
            if point.y < 0 or point.y >= len(self.graph):
                return False
            return True

        # If this fails for any reason the point is not in the graph
        except:
            return False

    def create_map(self):

        # Read in map from map.csv file
        print("Reading from map file \"map.csv\"")
        with open("map.csv") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                int_row = [ int(value) for value in row]
                self.map_2D.append(int_row)

        # At this point we have a 2D vector mapping, initialize graph
        print("Initializing 2D map")
        for y in range(0, len(self.map_2D)):
            self.graph.append([])
            for x in range(0, len(self.map_2D[y])):
                node = tree_node(self.map_2D[y][x], point(x, y), None, [])

                # Check for start node
                if node.value == CONST_START:
                    self.start = node

                # Check for goal node
                if node.value == CONST_GOAL:
                    self.goal = node

                # Add empty node to tree
                self.graph[y].append(node)

        # Free map_2D as it is no longer needed
        self.free_map_2D()

        # Add graph edges
        print("Initializing node tree")
        for y in range(0, len(self.graph)):
            for x in range(0, len(self.graph[y])):
                
                # Add edges based on connectedness
                if self.eight_connected:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):

                            # Check if the point is a valid location
                            node_addr = point(x + dx, y + dy)
                            if self.in_graph(node_addr):
                                if self.graph[node_addr.y][node_addr.x] != CONST_OBSTACLE:
                                    self.graph[y][x].adjacency_list.append(self.graph[node_addr.y][node_addr.x])

                else:
                    pass # Will have to impliment 4-connected graph

    def calculate_path(self):

        # Set starting point
        print("Calculating path...")
        nodes_to_visit = [self.start]
        goal_found = False

        while not goal_found and len(nodes_to_visit) > 0:

            # Get current node
            current_node = nodes_to_visit.pop()
            current_node.visited = True

            # Add adjacent nodes to the list of nodes to visit
            for node in current_node.adjacency_list:

                # Check if node is the goal
                if current_node == self.goal:
                    goal_found = True
                    break
                
                # Add new nodes to the list of nodes to visit
                if not node.visited and node.value != CONST_OBSTACLE:
                    if node not in nodes_to_visit:
                        
                        # Add the nodes parent, and append it to the list of nodes to visit
                        node.parent = current_node
                        nodes_to_visit.insert(0, node)

        # Check if a path exists
        if not goal_found:
            print("Goal Unreachable")
            sys.exit()

        # Find path
        path = []
        current_node = self.goal
        while current_node.parent != None:

            # Update path
            path.append(current_node.address)
            current_node = current_node.parent
        
        # Add start
        path.append(self.start.address)

        return path
