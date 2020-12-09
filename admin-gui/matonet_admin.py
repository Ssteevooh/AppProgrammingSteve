# -*- coding: utf-8 -*-
__author__ = "topseli"
__license__ = "0BSD"

import sys
import os
import socket
import threading
import base64
import logging
from PyQt5 import QtWidgets, uic
import login_view


class MatonetAdmin(QtWidgets.QWidget):

    def __init__(self):
        super(MatonetAdmin, self).__init__()
        self.init_ui()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.thread = threading.Thread(target=self.server_listener, args=(1,), daemon=True)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/main_window.ui'
        uic.loadUi(path, self)

        # Create QWidget instances
        self.login_widget = login_view.LoginView()

        # Add QWidget instances to stackedWidget
        self.stacked_widget.addWidget(self.login_widget)


        # Connect exit_buttons
        self.login_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)

        # Connect signals
        self.login_widget.login_signal.connect(
            self.on_login_clicked)

    def on_exit_button_clicked(self):
        sys.exit(0)

    def on_login_clicked(self, login_info):

        try:
            self.server.connect((login_info["address"], login_info["port"]))
            self.server.sendall(self.login_info["username"])

        except ConnectionRefusedError as e:
            self.login_widget.show_warning(e)
            return

        # self.stacked_widget.setCurrentWidget(self.admin_widget)
        # self.admin_widget_thread()

    def on_send_clicked(self, message):
        self.server.sendall(self.to_base64(message))


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = MatonetAdmin()
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
