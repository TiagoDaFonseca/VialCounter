"""

Module that controls usb camera

"""
import cv2


class WebCamera:
    def __init__(self, channel):
        self.capture = cv2.VideoCapture(channel)

    def grab_image(self):
        try:
            _, frame = self.capture.read()
            return frame
        except Exception as e:
            print(e)
            return None

    def close_camera(self):
        self.capture.release()
