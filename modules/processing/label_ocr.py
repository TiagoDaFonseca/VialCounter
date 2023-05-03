"""

PROGRAM: Optical Character Recognition using Tesseract
AUTHOR : T Cunha

"""
import cv2
import numpy as np
import imutils
import pytesseract
import time

# Global parameters


# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# get rgb image
def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# get grayscale image
def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# thresholding
def thresholding(img):
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


# opening - erosion followed by dilation
def opening(img):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(img):
    return cv2.Canny(img, 200, 300)


def read_file(filename):
    return cv2.imread(filename)


def create_window(name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 800, 600)
    return name


def show_image(window, img):
    cv2.imshow(window, img)
    cv2.waitKey(0)


def find_label(img):
    # find contours
    conts, hierarch = cv2.findContours(img, 1, 2)
    
    for cont in conts:
        are = cv2.contourArea(cont)
        if are > 50000:
            r = cv2.minAreaRect(cont)
            break
    
    return r


def rotate_label(img, ang):
    return imutils.rotate(img, angle=ang)


def set_roi(r, img):
    w, h = r[1]
    box = cv2.boxPoints(r)
    box = np.int0(box)

    return img[box[0][0] + 100:box[0][0] + int(h) - 50, box[0][0] + 50:box[0][0] + int(w) - 460]


def read_label(img):
    # Pre-processing
    gray = get_grayscale(img)
    cv2.imshow("a", gray)
    cv2.waitKey(0)
    thresh = thresholding(gray)
    cv2.imshow("b", thresh)
    cv2.waitKey(0)
    op = opening(thresh)
    cv2.imshow("f", op)
    cv2.waitKey(0)

    # Label detection
    try:
        rect = find_label(op)
    except Exception as e:
        print(e)
        return None
    else:
        # rotate the label
        angle = abs(rect[2])
        rotated = rotate_label(thresh, angle)
        cv2.imshow("d", rotated)
        cv2.waitKey(0)
        # determine new region of interest
        rect = find_label(rotated)
        roi = set_roi(rect, rotated)
        cv2.imshow("e", roi)
        cv2.waitKey(0)
    finally:
        # OCR
        return pytesseract.image_to_string(roi)

    #win = create_window("result")
    #show_image(win, roi)




def clean_text(lines):
    if '' in lines:
        lines.remove('')
    if ' ' in lines:
        lines.remove(' ')
    lines.pop(-1)
    return lines

"""
UNIT TEST
"""
if __name__ == "__main__":
    print("Init")

    # Reads image
    image = cv2.imread("/Users/tiagocunha/Code/VialCounter/test/label1.jpeg")

    start = time.process_time()

    # Process image
    text = read_label(image)
    words = text.split('\n')
    result = clean_text(words)

    end = time.process_time() - start

    print("elapsed time:", end)
    print(result)
