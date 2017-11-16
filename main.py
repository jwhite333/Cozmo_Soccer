import sys
import wavefront
import cozmoDirection
import cozmo

def main(robot: cozmo.robot.Robot):
    map = wavefront.map_object()
    map.create_map()
    path = map.calculate_path()

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

        # Print to indicate direction of motion
        print("Moving from point: {} to point: {}".format(current_point.printable(), next_point.printable()))

        motion.pointDirection(robot, next_point, current_point)
        current_point = next_point

    # Reached goal
    #motion.goal_reached(robot)

#if __name__ == "__main__":
#    main()

cozmo.run_program(main)