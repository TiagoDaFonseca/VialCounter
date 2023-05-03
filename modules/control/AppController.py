import threading
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThreadPool, QObject, QTimer, QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage
from modules.control import Workers
from modules.database import mongo
from modules.configuration import set_config
from modules.helpers.docs import list_docs, prep_docs_to_report
from modules.helpers.pdf import Report


def clean_dum_chars(lst):
    l3 = []
    for item in lst:
        if item != '':
            l3.append(item)
    return l3


def equal_words(lstRef, lst2):
    L = len(lstRef)
    print(L)
    if L == len(lst2):
        count = 0
        i=0
        for i in range(0, len(lstRef)):
            if lstRef[i] == lst2[i]:
                count+=1
        if count == L:
            return True
        else:
            return False
    else:
        return False


class AppControllerSignals(QObject):
    label_image_signal = pyqtSignal(QPixmap, name="label")
    vials_image_signal = pyqtSignal(QPixmap, name="vials")
    result_signal = pyqtSignal(dict, name="result")
    product_signal = pyqtSignal(str, name="product")
    lot_signal = pyqtSignal(str, name="lot")
    product_updated = pyqtSignal(name="updated")
    db_data_signal = pyqtSignal(list, name="db_data")
    db_connection_status = pyqtSignal(bool, name="status")
    warning_signal = pyqtSignal(str, name="warning")
    settings_signal = pyqtSignal(dict, name="settings")
    mongo_failed_signal = pyqtSignal(bool, name="mongo_failed")
    info_signal = pyqtSignal(str, name="info")


class AppController(QObject):

    def __init__(self):
        super(AppController, self).__init__()
        self.setObjectName("AppController")
        self.app_signals = AppControllerSignals()
        self.is_inspecting = False
        self.label_image = None
        self.vials_image = None
        self.product_in_batch = None
        self.lot_in_batch = None
        self.product = None
        self.lot = None
        self.tray = None
        self.vials_number = ""
        self.last_ten_trays = []
        self.is_production_mode_on = False
        self.server_address = ""
        self.db_name = ""
        self.db_col = ""
        self.dir_reports = ""
        self.documents = []
        # initialize ThreadPool
        self.thread_pool = QThreadPool()

        # cam thread
        self.camera_man = Workers.CameraMan()
        self.camera_man.signals.result.connect(lambda images: self.images_output(images))
        self.camera_man.signals.finished.connect(self.worker_complete)
        self.camera_man.signals.error.connect(self.worker_error)

        # inspection
        self.inspector = Workers.Inspector()
        self.inspector.inspector_signals.result.connect(lambda results: self.inspection_output(results))
        self.inspector.inspector_signals.error.connect(self.worker_error)
        self.inspector.inspector_signals.finished.connect(self.worker_complete)

        # Instantiate timer
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.image_acquisition_on)
        self.timer.start()

        # Params
        self.dir_reports = set_config.load_directory()
        self.server_address, self.db_name, self.db_col = set_config.load_server_address()
        self.last_ten_trays = set_config.load_last_session()
        self.p1, self.p2, self.minR, self.maxR = set_config.load_camera_settings()
        self.params = [self.p1, self.p2, self.minR, self.maxR]
        self.inspector.params = self.params

        # initialize database to a local server
        srv = "mongodb://" + self.server_address + "/"
        self.db = mongo.MongoDB(self.db_name, self.db_col, address=srv)
        was_connected = self.db.test_connection(srv)
        self.app_signals.mongo_failed_signal.emit(not was_connected)
        # result = self.db.test_connection("127.0.0.1")
        # print("TEST: " + str(result))

    def image_acquisition_on(self):
        if not self.is_inspecting:
            self.camera_man.run()

    @pyqtSlot(dict, name="inspection_result")
    def inspection_output(self, res):

        # images output
        images = {"label_image": res["label"], "vials_image": res["tray"]}
        self.camera_man.signals.result.emit(images)

        # Label OCR
        text = res["text"]

        tray_number = "Label not found"
        for item in text:
            string = item.lower()
            if "tray no." in string:
                self.tray= string.split(": ")[1].upper()
                # break
            if "lot#:" in string:
                self.lot = string.split(": ")[1]
                if text.index(item) == 1:
                    self.product = text[0].split(": ")[1]
                else:
                    self.product = text[0].split(": ")[1]
                    for w in range(1, text.index(item)):
                        self.product += " " + text[w]
        self.vials_number = str(res["size"])
        # text output
        if self.lot == None: self.lot="No label"
        if self.tray == None: self.tray="No tray"
        
        out_lot = "Lot: " + self.lot
        out = "Tray: " + self.tray + " | Vials#: " + self.vials_number
        self.app_signals.result_signal.emit({"lot_reading": out_lot,
                                             "tray_reading": out})

    def images_output(self, images):
        self.label_image = images["label_image"]
        self.vials_image = images["vials_image"]

        # print(self.label_image.__class__, self.label_image.shape)
        self.app_signals.label_image_signal.emit(QPixmap.fromImage(QImage(self.label_image.data,
                                                                          self.label_image.shape[1],
                                                                          self.label_image.shape[0],
                                                                          QImage.Format_RGB888)))
        self.app_signals.vials_image_signal.emit(QPixmap.fromImage(QImage(self.vials_image.data,
                                                                          self.vials_image.shape[1],
                                                                          self.vials_image.shape[0],
                                                                          QImage.Format_RGB888)))

    def worker_complete(self):
        pass

    def worker_error(self):
        pass

    @pyqtSlot(name="start_batch")
    def on_start_signal(self):
        print("Start batch")
        self.is_production_mode_on = True
        # self.product_in_batch = self.product
        # self.lot_in_batch = self.lot

    @pyqtSlot(name="stop_batch")
    def on_stop_signal(self):
        print("Stop batch")
        self.is_production_mode_on = False
        self.product_in_batch = ""
        self.lot_in_batch = ""

    @pyqtSlot(name="read_tray")
    def on_read_signal(self):
        print("Read")
        self.is_inspecting = True
        #self.inspector.lbl_img = self.label_image
        #self.inspector.tray_img = self.vials_image

        # Testing
        import cv2
        self.inspector.lbl_img = cv2.imread("test/label1.jpeg")
        self.inspector.tray_img = cv2.imread("test/whiteflask.jpg")
        self.inspector.run()

    @pyqtSlot(name="confirm_tray")
    def on_confirm_signal(self):
        print("Confirm")
        if self.is_production_mode_on:
            reading = clean_dum_chars(self.product.lower().split(' '))
            batch = clean_dum_chars(self.product_in_batch.lower().split(' '))
            print(batch)
            if equal_words(batch, reading):
                if self.lot.lower() == self.lot_in_batch.lower():
                    if self.tray.lower() not in self.last_ten_trays:
                        self.db.insert_one({"product": self.product,
                                            "lot": self.lot,
                                            "tray": self.tray,
                                            "vials": self.vials_number})
                        self.last_ten_trays.append(self.tray.lower())
                        if len(self.last_ten_trays) > 10:
                            self.last_ten_trays.pop(0)
                    else:
                        self.app_signals.warning_signal.emit("Tray already in database.")
                else:
                    self.app_signals.warning_signal.emit("Not from this batch. Please check the lot in current batch.")
            else:
                self.app_signals.warning_signal.emit("Please check product in batch")
        self.is_inspecting = False
        print("Done")

    @pyqtSlot(list, name="update_params")
    def on_cam_params_updated(self, prms):
        self.p1 = prms[0]
        self.p2 = prms[1]
        self.minR = prms[2]
        self.maxR = prms[3]

    @pyqtSlot(name="exit")
    def on_exit_application(self):
        usr, password = set_config.load_credentials()
        set_config.save_session(self.last_ten_trays,
                                self.p1,
                                self.p2,
                                self.minR,
                                self.maxR,
                                self.server_address,
                                self.dir_reports,
                                self.db_name,
                                self.db_col,
                                usr,
                                password
        )
        # self.app_signals.info_signal.emit("The system will now close.")
        QApplication.quit()

    @pyqtSlot(name="update_product")
    def on_update_signal(self, info):
        self.product_in_batch = info["product"]
        self.lot_in_batch = info["lot"]
        # self.app_signals.product_updated.emit()
        # print("product: " + self.product, "lot: " + self.lot)

    # DATABASE SLOTS
    @pyqtSlot(name="find all")
    def db_find_all(self):
        self.documents = list(self.db.find_all())
        self.app_signals.db_data_signal.emit(self.documents)

    @pyqtSlot(name="filter")
    def db_find(self, keywords):
        self.documents = list(self.db.find(keywords))
        print(self.documents)
        if len(self.documents)>0:
            # print(documents)
            self.app_signals.db_data_signal.emit(self.documents)
        else:
            print("no documents found")

    @pyqtSlot(str, name="test_connection")
    def check_db_connection(self, ip):
        res = self.db.test_connection(ip)
        self.app_signals.db_connection_status.emit(res)

    @pyqtSlot(name="export_signal")
    def create_report(self):
        lst = list_docs(self.documents)
        data = prep_docs_to_report(lst)
        pdf = Report()
        d = self.documents[0]
        # print(d['product'])
        prod = d['product']
        lot = d['lot']
        pdf.fill_report(product_name=prod, lot_number=lot, data=data)
        prod = prod.replace(' ', '_')
        lot = lot.replace(' ', '_')
        filename = '/' + prod + lot + ".pdf"
        # print(filename)
        pdf.output(self.dir_reports +  filename)
        self.app_signals.info_signal.emit("Report created.")

    @pyqtSlot(name="get_settings")
    def show_settings(self):
        sett = {"server": self.server_address, "dir": self.dir_reports}
        self.app_signals.settings_signal.emit(sett)

    @pyqtSlot(dict, name="change_settings")
    def on_change_settings(self, settings):
        self.server_address = settings["ip"]
        self.dir_reports = settings["dir"]
        # initialize database to a local server
        srv = "mongodb://" + self.server_address + "/"
        try:
            self.db.update_connection(srv, self.db_name, self.db_col)
            was_connected = True
        except Exception as e:
            # print(str(e))
            was_connected = False
            self.app_signals.warning_signal.emit("Database connection failed.")
        self.app_signals.mongo_failed_signal.emit(not was_connected)