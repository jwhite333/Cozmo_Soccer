import cv2
import numpy
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

min_object_radius = 10
screen_mid = 150

# Narrow range for goalie
left_of_screen_small = 115
right_of_screen_small = 185

# Wide range for kicker
left_of_screen_wide = 75
right_of_screen_wide = 225

def display_image(cv2_image):

    # Display video from camera
    cv2.imshow("Cozmo Camera", cv2_image)
    cv2.waitKey(1)

def detect_circle(image):

    # Get raw image
    raw_image = image.raw_image
    color_image = numpy.array(raw_image)
    bw_image = cv2.cvtColor(numpy.array(raw_image), cv2.COLOR_RGB2GRAY)

    # Blur
    bw_image = cv2.GaussianBlur(bw_image, (5, 5), 0)
    bw_image = cv2.medianBlur(bw_image, 5)

    # Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
    bw_image = cv2.adaptiveThreshold(bw_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 3.5)

    #kernel = numpy.ones((3,3),numpy.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    bw_image = cv2.erode(bw_image, kernel, iterations = 1)

    # Dilate
    bw_image = cv2.dilate(bw_image, kernel, iterations = 1)

    # Detect circles in the image
    circles = cv2.HoughCircles(bw_image, cv2.HOUGH_GRADIENT, 1, 200, param1=75, param2=45, minRadius=0, maxRadius=0)

    # Ensure at least some circles were found
    largest_circle = None
    if circles is not None:

        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = numpy.round(circles[0, :]).astype("int")
    
        # Loop over the (x, y) coordinates and radius of the circles
        largest_radius = 0.0
        for (x, y, r) in circles:
            # Draw the circle in the output image, then draw a rectangle in the image
            # Corresponding to the center of the circle
            cv2.circle(bw_image, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(bw_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # Check if this circle is the largest one found
            if r > largest_radius:
                largest_circle = (x, y, r)

    display_image(bw_image)

    return largest_circle

def detect_object(image):

    # Get frame as raw image
    raw_image = image.raw_image
    current_frame = cv2.cvtColor(numpy.array(raw_image), cv2.COLOR_RGB2BGR)

    # BGR range for orange
    color_lower = (0, 70, 225)
    color_upper = (130, 170, 255)

    # Works on 5th floor ISEC
    #color_lower = (0, 75, 225)
    #color_upper = (130, 170, 255)

    # Localize the object and remove imperfections
    mask = cv2.inRange(current_frame, color_lower, color_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    largest_circle = None

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
        if radius > min_object_radius:
            cv2.circle(current_frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(current_frame, centroid, 5, (0, 0, 255), -1)
            largest_circle = (x, y, radius)

    display_image(current_frame)

    return largest_circle