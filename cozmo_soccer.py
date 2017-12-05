# Nicolas Binford
# Uses the following programs as a reference:
# Cozmotography - Edge Detection
# https://github.com/cozplay/cozplay-demos/tree/master/cozmotography-edge-detection
# Adrian Rosebrock - Ball Tracking with OpenCV
# https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/


import os
import time
import cv2
import numpy
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.exceptions import RobotBusy


class CozmoSoccer:
    def __init__(self):
        self._robot = None
        self.min_object_radius = 10
        self.left_of_screen = 75
        self.right_of_screen = 225

        cozmo.connect(self.run)

    # Finds the object on the camera and returns its centroid (x, y)
    def detect_object(self, current_frame):
        # BGR range for orange
        color_lower = (0, 100, 230)
        color_upper = (130, 170, 255)

        # Localize the object and remove imperfections
        mask = cv2.inRange(current_frame, color_lower, color_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in the object
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]

        # If at least one contour was found
        if len(cnts) > 0:
            # Get the largest contour by area
            largest_contour = max(cnts, key=cv2.contourArea)

            # Calculate the centroid using the moments of the largest contour
            # Centroid is coordinates with 0, 0 being at the top left
            M = cv2.moments(largest_contour)
            centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Calculate the minimum enclosing circle
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

            # If the object is close enough, draw its centroid and enclosing circle
            # on the frame
            if radius > self.min_object_radius:
                cv2.circle(current_frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(current_frame, centroid, 5, (0, 0, 255), -1)
                return centroid
            else:
                return None

    def follow_ball(self, centroid):
        if centroid is not None:
            # Get x-coordinate of centroid
            x_direction = centroid[0]
            # If ball is to the left of image
            if x_direction <= self.left_of_screen:
                try:
                    self._robot.turn_in_place(degrees(20))
                except RobotBusy:
                    pass
            # If ball is in the middle of image
            elif x_direction <= self.right_of_screen:
                try:
                    self._robot.drive_straight(distance_mm(30), speed_mmps(100), should_play_anim=False)
                except RobotBusy:
                    pass
            # If ball is to the right of image
            else:                
                try:
                    self._robot.turn_in_place(degrees(-20))
                except RobotBusy:
                    pass

    def on_new_camera_image(self, event, *, image:cozmo.world.CameraImage, **kw):
        raw_image = image.raw_image

        # Convert PIL Image to OpenCV Image
        # See: http://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
        cv2_image = cv2.cvtColor(numpy.array(raw_image), cv2.COLOR_RGB2BGR)

        ball_center = self.detect_object(cv2_image)
        self.follow_ball(ball_center)

        # Display video from camera
        cv2.imshow("Cozmo Camera", cv2_image)
        cv2.waitKey(1)

    def set_up_cozmo(self, coz_conn):
        self._robot = coz_conn.wait_for_robot()
        self._robot.camera.image_stream_enabled = True
        # Color camera is disabled by default, have to enable it
        self._robot.camera.color_image_enabled = True
        self._robot.add_event_handler(cozmo.world.EvtNewCameraImage, self.on_new_camera_image)
        self._robot.set_head_angle(cozmo.util.Angle(degrees=0))

    def run(self, coz_conn):
        self.set_up_cozmo(coz_conn)
        while True:
            # Have to do ctrl+C to exit
            time.sleep(0)


if __name__ == '__main__':
    CozmoSoccer()

