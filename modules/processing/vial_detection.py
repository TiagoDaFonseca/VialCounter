import numpy as np
import cv2
import time

# Global parameters
# p1 = 200
# p2 = 25  # IF we tune this to 30 and control illumination we can use these params as they are to every batch :D
# minR = 20  # parameter to tune
# maxR = 40  # parameter to tune
# minDist = 2 * minR  # This is the problematic parameter


# Functions
def bgr2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def rgb2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def detect_circles(img, par1, par2, min_rad, max_rad):
    # Detect circles
    circs = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, minDist=2*min_rad, param1=par1, param2=par2, minRadius=min_rad,
                             maxRadius=max_rad)
    return circs


def draw_circles(img, circs):
    # convert the (x, y) coordinates and radius of the circles to integers
    cs = np.round(circs[0, :]).astype("int")
    sz = 0
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in cs:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(img, (x, y), r, (0, 255, 0), 4)
        sz = sz + 1
    return sz


if __name__ == "__main__":
    print("Init vial detection")

    """
    Initial functions for testing
    """
    # Relative path of the images
    filename = "/Users/tiagocunha/Documents/PycharmProjects/VialCounter/test/blueflask.jpg"

    # Reads image
    image = cv2.imread(filename)
    """
    Image processing
    """
    print("Init")

    start = time.process_time()
    # Creates a copy
    output = image.copy()
    gray = bgr2gray(output)

    # Detect circles
    circles = detect_circles(gray, 200, 25, 20, 40)

    # ensure at least some circles were found
    if circles is not None:
        size = draw_circles(image, circles)
    else:
        size = 0

    dt = time.process_time() - start
    print("Processing time", dt)
    print("Number: " + str(size))

    # # show the output image. hstack piles both images side by side
    imS = cv2.resize(np.hstack([image, output]), (960, 540))  # Resize image
    # # show result
    cv2.imshow("result", imS)
    cv2.waitKey(0)
