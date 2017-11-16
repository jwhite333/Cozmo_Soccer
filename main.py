import sys
import wavefront
import cozmoDirection

def main():
    map = wavefront.map_object()
    map.create_map()
    path = map.calculate_path()

    for location in path:
        print("Path step: ", location.printable())

    # Initialize movement object
    motion = cozmoDirection.cozmo_motion()

    # Begin at the start position
    current_point = path.pop()

    # Check if we are at the goal
    if len(path) == 0:
        motion.goal_reached()
        sys.exit()

    # Move to next point
    while len(path) > 0:
        next_point = path.pop()
        motion.pointDirection(next_point, current_point)
        current_point = next_point


if __name__ == "__main__":
    main()