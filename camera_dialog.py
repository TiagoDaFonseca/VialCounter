"""

PROGRAM: Camera Dialog version 0.1
AUTHORS: T Cunha & P Riscado

"""
# Modules
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import sys
import numpy as np
import uis.resources.resources  # CAUTION DONT ERASE
from modules.processing import label_ocr, vial_detection
from modules.configuration.set_config import load_camera_settings


def process_image(img, p1, p2, minR, maxR):
    # vial detection

    try:
        im = vial_detection.bgr2rgb(img)
        gray = vial_detection.rgb2gray(im)
        circles = vial_detection.detect_circles(gray,
                                                p1,
                                                p2,
                                                minR,
                                                maxR)
    except Exception as e:
        print(e)
    else:
        # Vial counting
        size = 0
        if circles is not None:
            size = vial_detection.draw_circles(im, circles)
        print(size, "circles found")
    finally:
        return im


class CamUI(QDialog):
    def __init__(self):
        super(CamUI, self).__init__()
        uic.loadUi("uis/camera.ui", self)
        self.setWindowTitle("Cam Settings - Vial Counter v0.1")
        p1, p2, minr, maxr = load_camera_settings()
        self.params = [p1, p2, minr, maxr]
        self.is_tuning = False

        # Buttons
        self.buttonBox = self.findChild(QDialogButtonBox, "buttonBox")

        # Sliders
        self.param1 = self.findChild(QSlider, "Param1Slider")
        self.param2 = self.findChild(QSlider, "Param2Slider")
        self.min_radius = self.findChild(QSlider, "MinRSlider")
        self.max_radius = self.findChild(QSlider, "MaxRSlider")

        # Labels
        self.param1_lbl = self.findChild(QLabel, "param1_label")
        self.param2_lbl = self.findChild(QLabel, "param2_label")
        self.minR_lbl = self.findChild(QLabel, "minR_label")
        self.maxR_lbl = self.findChild(QLabel, "maxR_label")

        self.param1.setValue(self.params[0])
        self.param2.setValue(self.params[1])
        self.min_radius.setValue(self.params[2])
        self.max_radius.setValue(self.params[3])
        self.param1_lbl.setText(str(self.params[0]))
        self.param2_lbl.setText(str(self.params[1]))
        self.minR_lbl.setText(str(self.params[2]))
        self.maxR_lbl.setText(str(self.params[3]))

        # Segmented Image
        self.cam_window_image = self.findChild(QLabel, "segmentation_image")

        # Connections
        self.param1.valueChanged.connect(self.set_param1)
        self.param2.valueChanged.connect(self.set_param2)
        self.min_radius.valueChanged.connect(self.set_min_radius)
        self.max_radius.valueChanged.connect(self.set_max_radius)

    def set_param1(self):
        #print(self.param1.value())
        self.params[0] = int(self.param1.value())
        self.param1_lbl.setText(str(self.params[0]))

    def set_param2(self):
        #print(self.param2.value())
        self.params[1] = int(self.param2.value())
        self.param2_lbl.setText(str(self.params[1]))

    def set_min_radius(self):
        #print(self.min_radius.value())
        self.params[2] = int(self.min_radius.value())
        self.minR_lbl.setText(str(self.params[2]))

    def set_max_radius(self):
        #print(self.max_radius.value())
        self.params[3] = int(self.max_radius.value())
        self.maxR_lbl.setText(str(self.params[3]))

    @pyqtSlot(np.ndarray, name="tune")
    def update_image(self, img):
        if self.is_tuning:
            p_img = process_image(img, self.params[0], self.params[1], self.params[2], self.params[3])
            self.cam_window_image.setPixmap(QPixmap.fromImage(QImage(p_img.data,
                                                                     p_img.shape[1],
                                                                     p_img.shape[0],
                                                                     QImage.Format_RGB888)))
        else:
            self.cam_window_image.setPixmap(QPixmap.fromImage(QImage(img.data,
                                                                     img.shape[1],
                                                                     img.shape[0],
                                                                     QImage.Format_RGB888)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CamUI()
    window.showFullScreen()
    sys.exit(app.exec_())
