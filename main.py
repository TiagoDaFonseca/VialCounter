
import sys
import mainwindow as ui
import camera_dialog
from modules.control.AppController import AppController


# MAIN FUNCTION
if __name__ == "__main__":

    app = ui.QApplication(sys.argv)
    app.setApplicationName("Vial Counter v0.1")
    app.setOrganizationName("X2")
    window = ui.UI()

    # Create a parallel event loop for business logic control
    controller = AppController()
    control_thread = ui.QThread()
    controller.moveToThread(control_thread)

    ''' Connections '''
    # Actions to take in controller
    window.update_signal.connect(lambda info: controller.on_update_signal(info))
    window.start_signal.connect(controller.on_start_signal)
    window.stop_signal.connect(controller.on_stop_signal)
    window.read_signal.connect(controller.on_read_signal)
    window.confirm_signal.connect(controller.on_confirm_signal)
    window.exit_signal.connect(controller.on_exit_application)
    window.update_camera_params_signal.connect(controller.on_cam_params_updated)
    window.get_settings.connect(controller.show_settings)
    window.settings_dlg.signals.test_connection_signal.connect(lambda x: controller.check_db_connection(x))
    window.change_settings_signal.connect(lambda x: controller.on_change_settings(x))
    window.database_dlg.db_signals.export_signal.connect(controller.create_report)

    # Actions to take place in main window
    controller.app_signals.label_image_signal.connect(lambda x: window.update_label_image(x))
    controller.app_signals.vials_image_signal.connect(lambda x: window.update_vials_image(x))
    controller.app_signals.product_signal.connect(lambda x: window.show_current_product(x))
    controller.app_signals.lot_signal.connect(lambda x: window.show_current_lot(x))
    controller.app_signals.result_signal.connect(lambda x: window.update_result(x))
    controller.inspector.inspector_signals.result.connect(lambda res: controller.inspection_output(res))
    controller.app_signals.product_updated.connect(window.is_product_updated)
    controller.app_signals.warning_signal.connect(lambda x: window.show_warning(x))
    controller.app_signals.settings_signal.connect(lambda x: window.settings_dlg.on_settings_changed(x))
    controller.app_signals.db_connection_status.connect(lambda x: window.settings_dlg.on_connection_status(x))
    controller.app_signals.mongo_failed_signal.connect(lambda x: window.on_mongo_failed(x))
    controller.app_signals.info_signal.connect(lambda x: window.show_information(x))

    # Actions to take place in camera dialog
    controller.camera_man.signals.img2tune.connect(lambda x: window.camera_dlg.update_image(x))

    # Actions to take place in database dialog
    window.db_find_signal.connect(controller.db_find_all)
    window.database_dlg.db_signals.searchAll_signal.connect(controller.db_find_all)
    window.database_dlg.db_signals.filter_signal.connect(lambda x: controller.db_find(x))
    # window.database_dlg.update_table_signal()
    # window.database_dlg.filter_signal()
    controller.app_signals.db_data_signal.connect(lambda dt: window.database_dlg.update_data(dt))
    # Warning to take place (feedback from controller to window)

    # Start application
    control_thread.start()
    window.showFullScreen()

    # When Quit application
    sys.exit(app.exec_())
