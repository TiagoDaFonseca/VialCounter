from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys


class PassUI(QDialog):
    def __init__(self):
        super(PassUI, self).__init__()
        uic.loadUi("uis/credentials.ui", self)
        self.setWindowTitle("Authorization - Vial Counter v0.1")
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        self.usr = ""
        self.passwrd = ""

        # line Edits
        self.user = self.findChild(QLineEdit, "user")
        self.password = self.findChild(QLineEdit, "password")
        self.buttonBox = self.findChild(QDialogButtonBox, "buttonBox")

        self.user.textChanged.connect(self.check_usr)
        self.password.textChanged.connect(self.check_pass)
        self.buttonBox.accepted.connect(self.accept)

    def check_usr(self):
        self.usr = self.user.text()

    def check_pass(self):
        self.passwrd = self.password.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassUI()
    window.show()
    r = window.exec_()
    print(r)
