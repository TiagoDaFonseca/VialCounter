from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtWidgets import QMainWindow, QTableView, QApplication, QHeaderView



class InspectionModel (QAbstractTableModel):

    def __init__(self, data):
        super(InspectionModel, self).__init__()
        self._data = data  # lista de Bson Documents
        self._keys = list(data[0].keys())

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._keys[section].title()

    def data(self, index, role):
        row = self._data[index.row()]
        column = self._keys[index.column()]
        if index.column() == 0:
            curr_row = self._data[index.row()]['_id']
            return str(curr_row)#['$oid'])
        elif role == Qt.DisplayRole:
            return row[column]
        # ADDED LINES
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        ###

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._keys)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = [{"_id": {"$oid": "5f34418b9d0bb937a2108ac0"},
                 "product": "Vancomycin Hydrochloride",
                 "lot": "2001039.1",
                 "tray": "T0104",
                 "vials": "287"
                 },
                {"_id": {"$oid": "5f34418b9d0bb937a2108ac1"},
                 "product": "Vancomycin Hydrochloride",
                 "lot": "2001039.1",
                 "tray": "T0104",
                 "vials": "180"
                 }]

        self.model = InspectionModel(data)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setCentralWidget(self.table)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
