"""

PROGRAM: Vial Counter version 0.1
AUTHORS: T Cunha & P Riscado

"""
# Modules
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import sys
from camera_dialog import CamUI
from database_dialog import DatabaseUI
from settings_dialog import SettingsUI
from credentials_dialog import PassUI
from modules.configuration import set_config
import uis.resources.resources  # ATTENTION: it is being used by mainwindow.ui
########################################################################################################################


class UI(QMainWindow):

    product_name = ""
    product_lot = ""

    ''' List signals '''
    # Signals for batch settings
    start_signal = pyqtSignal(name='start_batch')
    stop_signal = pyqtSignal(name='stop_batch')
    update_signal = pyqtSignal(dict, name='update_product')
    # signals for process
    read_signal = pyqtSignal(name='read_tray')
    confirm_signal = pyqtSignal(name='confirm_tray')
    db_find_signal = pyqtSignal(name="find all")
    exit_signal = pyqtSignal(name="exit")
    update_camera_params_signal = pyqtSignal(list, name="update_params")
    get_settings = pyqtSignal(name="get_settings")
    change_settings_signal = pyqtSignal(dict, name="change_settings")

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("uis/mainwindow.ui", self)
        self.setWindowTitle("Vial Counter v0.5")
        self.mongo_failed = False
        self.production_mode_is_on = False

        # dialogs
        self.database_dlg = DatabaseUI()
        self.camera_dlg = CamUI()
        self.settings_dlg = SettingsUI()
        self.credentials_dlg = PassUI()
        ''' List widgets '''
        # Menu Buttons
        self.camera_settings_button = self.findChild(QPushButton, "camera_settings_button")
        #self.reports_button = self.findChild(QPushButton, "reports_button")
        self.database_button = self.findChild(QPushButton, "database_button")
        self.general_settings_button = self.findChild(QPushButton, "general_settings_button")

        # Process Buttons
        self.confirm_tray_button = self.findChild(QPushButton, "confirm_tray_button")
        self.read_tray_button = self.findChild(QPushButton, "read_tray_button")
        self.stop_batch_button = self.findChild(QPushButton, "stop_batch_button")
        self.start_batch_button = self.findChild(QPushButton, "start_batch_button")
        self.update_product_button = self.findChild(QPushButton, "update_product_button")
        self.shutdown_button = self.findChild(QPushButton, "shutdown_button")

        # Labels
        self.result_box = self.findChild(QGroupBox, "inspection_box")
        self.result = self.result_box.findChild(QLabel, "result")
        # print(self.result.__class__)
        self.lote = self.findChild(QLabel, "lote")
        # print(self.lote.__class__)

        self.result.setText("Result will appear here")
        self.tray_image = self.findChild(QLabel, "tray_image")
        self.label_image = self.findChild(QLabel, "box_label_image")
        self.time = self.findChild(QLabel, "time_label")

        # line Edits
        self.product = self.findChild(QLineEdit, "product_parameter")
        self.lot = self.findChild(QLineEdit, "lot_parameter")
        self.product.setPlaceholderText("Enter your product")
        self.lot.setPlaceholderText("Enter your lot#")

        # status bar
        self.status = self.findChild(QStatusBar, "statusBar")
        self.setStatusBar(self.status)

        # Set time
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.print_date)
        self.timer.start()

        # Connections
        self.camera_settings_button.clicked.connect(self.open_camera_settings_dialog)
        #self.reports_button.clicked.connect(self.open_reports_dialog)
        self.database_button.clicked.connect(self.open_database_dialog)
        self.general_settings_button.clicked.connect(self.open_general_settings_dialog)

        self.confirm_tray_button.clicked.connect(self.confirm_tray)
        self.read_tray_button.clicked.connect(self.read_tray)
        self.product.textChanged.connect(self.update_product)
        self.lot.textChanged.connect(self.update_product)
        self.start_batch_button.clicked.connect(self.start_batch)
        self.stop_batch_button.clicked.connect(self.stop_batch)
        # self.update_product_button.clicked.connect(self.update_product)

        self.shutdown_button.clicked.connect(self.exit_signal.emit)# QApplication.quit)

        self.show_message("INTERFACE IS LOADED :D ENJOY")

    ####################################################################################################################

    @pyqtSlot(bool, name="mongo_failed")
    def on_mongo_failed(self, state):
        self.mongo_failed = state

    @pyqtSlot(str, name="warning")
    def show_warning(self, warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(warning)
        # msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()

    @pyqtSlot(str, name="info")
    def show_information(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.NoIcon)
        msg.setText(message)
        # msg.setInformativeText('More information')
        msg.setWindowTitle("Info")
        msg.exec_()

    def confirm_tray(self):
        self.confirm_signal.emit()
        self.result.setText("Result will be here")
        self.lote.setText("")
        # Define the actions to take during production mode:
        # check if this inspection already exists
        # if not save it to database

    def read_tray(self):
        self.read_signal.emit()
        self.label_image.clear()
        self.tray_image.clear()
        self.result.setText("Waiting for results")

    def set_buttons_settings(self, state):
        if state is True:
            # self.update_product_button.setText("DISABLED")
            # self.update_product_button.setEnabled(False)
            msg = "Production mode is on. Inspections will be added to database from now on."
            self.start_batch_button.setEnabled(False)
            self.show_information(msg)
            # self.start_batch_button.setStyleSheet('QPushButton {background-color: green; color: white;}')
        else:
            # self.update_product_button.setText("UPDATE")
            # self.update_product_button.setEnabled(True)
            msg = "Production mode is off. Inspections will be discarded."
            self.start_batch_button.setEnabled(True)
            self.show_information(msg)
        # self.product.setReadOnly(state)
        # self.lot.setReadOnly(state)

    def start_batch(self):
        self.production_mode_is_on = True
        self.show_message("PRODUCTION MODE IS ON")
        if (self.product.text() != "") and (self.lot.text() != ""):
            self.update_signal.emit({"product": self.product.text(),
                                     "lot": self.lot.text()})
            self.set_buttons_settings(True)
            self.start_signal.emit()
            # msg = "Product and lot updated! You may proceed :)"
            # self.show_message()
            # self.show_information(msg)
        else:
            wrg = "Product and lot cannot be empty my old friend"
            self.show_warning(wrg)

    def stop_batch(self):
        self.production_mode_is_on = False
        self.show_message("PRODUCTION MODE IS OFF")
        self.set_buttons_settings(False)
        self.stop_signal.emit()

    def update_product(self):
        if self.production_mode_is_on:
            if (self.product.text() != "") and (self.lot.text() != ""):
                self.update_signal.emit({"product": self.product.text(),
                                         "lot": self.lot.text()})

    def open_camera_settings_dialog(self):
        is_authorized = self.open_credentials_dialog()
        if is_authorized:
            self.confirm_signal.emit()
            self.show_message("OPENING CAMERAS SETTINGS")
            if self.camera_dlg.isVisible():
                self.camera_dlg.raise_()
                self.activateWindow()
            else:
                self.camera_dlg.is_tuning = True
                self.camera_dlg.showFullScreen()
                is_ok = self.camera_dlg.exec()
                self.camera_dlg.is_tuning = False
                if is_ok:
                    print("Save params")
                    p1 = int(self.camera_dlg.param1.value())
                    p2 = int(self.camera_dlg.param2.value())
                    minR = int(self.camera_dlg.min_radius.value())
                    maxR = int(self.camera_dlg.max_radius.value())
                    prms = [p1,p2,minR,maxR]
                    self.update_camera_params_signal.emit(prms)
                    self.show_message("CAM PARAMS UPDATED")
                else:
                    p1, p2, minR, maxR = set_config.load_camera_settings()
                    self.camera_dlg.param1.setValue(p1)
                    self.camera_dlg.param2.setValue(p2)
                    self.camera_dlg.min_radius.setValue(minR)
                    self.camera_dlg.max_radius.setValue(maxR)
                    print("params discarded")
        else:
            self.show_warning("Wrong user or password")
        self.credentials_dlg.user.setText("")
        self.credentials_dlg.password.setText("")

    def open_credentials_dialog(self):
        usr, password = set_config.load_credentials()
        self.credentials_dlg.show()
        is_ok = self.credentials_dlg.exec_()
        print("res: ", is_ok)
        if is_ok:
            if self.credentials_dlg.usr.lower() == usr:
                if self.credentials_dlg.passwrd == password:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def open_reports_dialog(self):
        self.show_message("OPENING REPORTS CREATOR")

    def open_database_dialog(self):
        self.show_message("OPENING DATABASE WINDOW")
        if self.mongo_failed:
            self.show_warning("Please set server first.")
        else:
            if self.database_dlg.isVisible():
                self.database_dlg.raise_()
                self.database_dlg.activateWindow()
            else:
                self.db_find_signal.emit()
                self.database_dlg.show()

    def open_general_settings_dialog(self):
        is_authorized = self.open_credentials_dialog()
        if is_authorized:
            self.show_message("OPENING TOOLS WINDOW")
            if self.settings_dlg.isVisible():
                self.settings_dlg.raise_()
                self.settings_dlg.activateWindow()
            else:
                self.get_settings.emit()
                self.settings_dlg.show()
                is_ok = self.settings_dlg.exec()
                if is_ok:
                    print("Save params")
                    self.change_settings_signal.emit({"ip": self.settings_dlg.db_server.text(),
                                                      "dir": self.settings_dlg.reports_path.text()})
                    self.show_message("CAM PARAMS UPDATED")
                else:
                    print("params discarded")
        else:
            self.show_warning("Wrong user or password")
        self.credentials_dlg.user.setText("")
        self.credentials_dlg.password.setText("")

    @pyqtSlot(dict, name="result")
    def update_result(self, sentences):
        # print(sentence)
        self.lote.setText(sentences["lot_reading"])
        self.result.setText(sentences["tray_reading"])

    @pyqtSlot(QPixmap, name="label")
    def update_label_image(self, x):
        self.label_image.setPixmap(x)

    @pyqtSlot(QPixmap, name="vials")
    def update_vials_image(self, x):
        self.tray_image.setPixmap(x)

    @pyqtSlot(str, name="product")
    def show_current_product(self, x):
        self.product.setText(x)
        self.show_message("PRODUCT AND LOT UPDATED")

    @pyqtSlot(str, name="lot")
    def show_current_lot(self, x):
        self.lot.setText(x)

    @pyqtSlot(name="updated")
    def is_product_updated(self):
        self.show_message("PRODUCT UPDATED")

    def show_message(self, msg):
        self.status.showMessage(msg, 5000)

    def print_date(self):
        self.time.setText(QDate.currentDate().toString(Qt.DefaultLocaleLongDate) + " | Local time: " +
                          QTime.currentTime().toString() + " ")

        self.update()
        QApplication.processEvents()


# UNIT TEST
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = UI()
    window.showFullScreen()
    sys.exit(app.exec_())

