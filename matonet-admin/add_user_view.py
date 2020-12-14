# -*- coding: utf-8 -*-
""" login_view.py - presenter for the login prompt"""
__author__ = "topseli"
__license__ = "0BSD"


import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox


class AddUserView(QtWidgets.QWidget):

    create_user_button_signal = pyqtSignal(dict)

    def __init__(self):
        super(AddUserView, self).__init__()
        self.init_ui()

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/add_user_view.ui'
        uic.loadUi(path, self)

    def show_warning(self, e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("The server is not responding")
        msg.setWindowTitle("Connection error")
        msg.setDetailedText(str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @pyqtSlot()
    def on_create_user_button_clicked(self):
        user_info = {
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }
        self.create_user_button_signal.emit(user_info)


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = AddUserView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
