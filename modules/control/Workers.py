from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
import cv2
from modules.sensors import webcamera as cam
from modules.processing import vial_detection, label_ocr
import numpy as np
from modules.sensors import picamera


class CameraManSignals(QObject):
    finished = pyqtSignal(name="camera_finished")
    error = pyqtSignal(str, name="camera_error")
    result = pyqtSignal(dict, name="camera_result")
    img2tune = pyqtSignal(np.ndarray, name="tune")


class CameraMan(QRunnable):
    """
    WORKER THREAD
    """
    def __init__(self):
        super(CameraMan, self).__init__();
        self.signals = CameraManSignals()
        self.camera4label = cam.WebCamera(0)
        self.camera4vials = None  # to initiate with picamera
        self.label_image = None
        self.vials_image = None
        #self.params = [0,0,0,0]
        # camera4vials = picamera.Picamera()

    @pyqtSlot()
    def run(self):
        """
         Loop that retrieves the images from camera
        :return: image to UI
        """
        try:
            self.label_image = self.camera4label.grab_image()

            self.vials_image = self.label_image
            self.signals.img2tune.emit(self.vials_image)

            self.label_image = cv2.cvtColor(self.label_image, cv2.COLOR_BGR2RGB)
            self.vials_image = self.label_image  # to grab image from picamera

        except Exception as e:
            self.signals.error.emit("ERROR CAMERA_MAN")
        else:
            self.signals.finished.emit()
            self.signals.result.emit({"label_image": self.label_image,
                                      "vials_image": self.vials_image})  # to send the vials image
        finally:
            self.signals.finished.emit()


class InspectorSignals(QObject):
    finished = pyqtSignal(name="inspection_finished")
    error = pyqtSignal(str, name="inspection_error")
    result = pyqtSignal(dict, name="inspection_result")


class Inspector(QRunnable):
    def __init__(self):
        super(Inspector, self).__init__()
        self.inspector_signals = InspectorSignals()
        self.tray_size = 0
        self.info = []
        self.tray_inspection = None
        self.label_inspection = None
        self.tray_img = None
        self.lbl_img = None
        self.params = [0,0,0,0]

    @pyqtSlot()
    def run(self):
        circles = None
        raw = ""

        try:

            # vial detection
            gray = vial_detection.bgr2gray(self.tray_img)
            self.tray_img = label_ocr.bgr2rgb(self.tray_img)
            circles = vial_detection.detect_circles(gray,
                                                    self.params[0],
                                                    self.params[1],
                                                    self.params[2],
                                                    self.params[3])
            # Label OCR
            raw = label_ocr.read_label(self.lbl_img)
        except Exception as e:
            print(e)
        else:
            # Vial counting
            if circles is not None:
                self.tray_size = vial_detection.draw_circles(self.tray_img, circles)
            else:
                self.tray_size = 0

            # Label Info
            if raw is not "":
                words = raw.split('\n')
                self.info = label_ocr.clean_text(words)
            else:
                self.info = None

        finally:
            # put some signals
            ocr = label_ocr.bgr2rgb(self.lbl_img)
            tray = self.tray_img
            res = {"label": ocr,
                   "text": self.info,  # list of tray info words
                   "tray": tray,
                   "size": self.tray_size}

            self.inspector_signals.result.emit(res)
            self.tray_img = None
            self.lbl_img = None

