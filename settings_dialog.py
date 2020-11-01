from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import os


def show_information(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.NoIcon)
    msg.setText(message)
    # msg.setInformativeText('More information')
    msg.setWindowTitle("Info")
    msg.exec_()


class SettingsSignals(QObject):
    test_connection_signal = pyqtSignal(str, name="test_connection")


class SettingsUI(QDialog):
    def __init__(self):
        super(SettingsUI, self).__init__()
        uic.loadUi("uis/settings.ui", self)
        self.signals = SettingsSignals()
        self.setWindowTitle("General Settings - Vial Counter v0.1")
        self.ip_address = ""

        # Buttons
        self.buttonBox = self.findChild(QDialogButtonBox, "buttonBox")
        self.test_connection_button = self.findChild(QPushButton, "test_connection_button")
        self.browse_button = self.findChild(QPushButton, "browse_button")

        # LineEdits
        self.db_server = self.findChild(QLineEdit, "db_server")
        self.reports_path = self.findChild(QLineEdit, "reports_path")

        self.test_connection_button.clicked.connect(self.test_connection)
        self.browse_button.clicked.connect(self.choose_folder)

    def test_connection(self):
        self.signals.test_connection_signal.emit(self.db_server.text())

    def choose_folder(self):
        # download_path = self.download_folder_lineEdit.text()
        folder_path = "/Users/tiagocunha/Documents/Reports"
        # open select folder dialog
        try:
            fname = QFileDialog.getExistingDirectory(
                self, 'Select a directory', folder_path)
        except Exception as e:
            print(str(e))

        if fname:
            # Returns pathName with the '/' separators converted to separators that are appropriate for the underlying operating system.
            # On Windows, toNativeSeparators("c:/winnt/system32") returns
            # "c:\winnt\system32".
            fname = QDir.toNativeSeparators(fname)

        if os.path.isdir(fname):
            self.reports_path.setText(fname)

    @pyqtSlot(bool, name="status")
    def on_connection_status(self, connected):
        if connected:
            show_information("connection is OK.")
        else:
            show_information("connection failed")

    @pyqtSlot(dict, name="settings")
    def on_settings_changed(self, setting):
        self.db_server.setText(setting["server"])
        self.reports_path.setText(setting["dir"])


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SettingsUI()
    window.show()
    sys.exit(app.exec_())