from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from modules.database.inspectionmodel import InspectionModel
from PyQt5 import uic
import sys


class DatabaseSignals(QObject):
    # Signals
    # update_table_signal = pyqtSignal()
    searchAll_signal = pyqtSignal(name="find all")
    filter_signal = pyqtSignal(dict, name="filter")
    export_signal = pyqtSignal(name="export_signal")


class DatabaseUI(QDialog):

    def __init__(self):
        super(DatabaseUI, self).__init__()
        uic.loadUi("uis/database.ui", self)
        self.setWindowTitle("Mongo Database - Vial Counter v0.1")
        self.filters = ['', '']
        self.db_signals = DatabaseSignals()

        # Buttons
        self.export_button = self.findChild(QPushButton, "export_button")
        self.filter_button = self.findChild(QPushButton, "filter_button")

        # LineEdits
        self.tray_search_bar = self.findChild(QLineEdit, "tray_search")
        self.lot_search_bar = self.findChild(QLineEdit, "lot_search")
        self.product_search_bar = self.findChild(QLineEdit, "product_search")

        # TableView
        self.tableview = self.findChild(QTableView, "tableView")
        self.model = None

        # Connections GUI
        self.filter_button.clicked.connect(self.on_filter_clicked)
        self.export_button.clicked.connect(self.on_export_clicked)

    @pyqtSlot(list, name='db_data')
    def update_data(self, data):
        self.model = InspectionModel(data)
        self.tableview.setModel(self.model)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def on_filter_clicked(self):
        self.filters = [self.product_search_bar.text(),
                        self.lot_search_bar.text(),
                        self.tray_search_bar.text()]

        if self.filters[0] == self.filters[1] == self.filters[2] == "":
            self.db_signals.searchAll_signal.emit()
        elif self.filters[0] != "" and self.filters[1] == self.filters[2] == "":
            f= {"product": self.filters[0]}
            self.db_signals.filter_signal.emit(f)
        elif self.filters[1] != "" and self.filters[0] == self.filters[2] == "":
            f = {"lot": self.filters[1]}
            self.db_signals.filter_signal.emit(f)
        elif self.filters[2] != "" and self.filters[1] == self.filters[0] == "":
            f = {"tray": self.filters[2]}
            self.db_signals.filter_signal.emit(f)
        else:
            f = {"product": self.filters[0],
                 "lot": self.filters[1],
                 "tray": self.filters[2]}
            self.db_signals.filter_signal.emit(f)

        print("Searching cenas")

    def on_export_clicked(self):
        self.db_signals.export_signal.emit()

    def save2csv(self):
        print("Saving to csv file")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseUI()
    window.show()
    sys.exit(app.exec_())
