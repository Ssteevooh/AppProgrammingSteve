# -*- coding: utf-8 -*-
""" user_view.py - presenter for the user table editor"""
__author__ = "topseli"
__license__ = "0BSD"


import os
import sys
import requests
from logger import log
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox


class UserView(QtWidgets.QWidget):

    keys = (
        "user_id",
        "role",
        "username",
        "password",
        "is_active",
        "created_at",
        "updated_at"
    )

    update_signal = pyqtSignal()
    product_signal = pyqtSignal()

    def __init__(self):
        super(UserView, self).__init__()
        self.init_ui()

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/user_view.ui'
        uic.loadUi(path, self)

    def show_warning(self, e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Invalid values")
        msg.setText("Check the values you entered\n" + str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def set_row(self, row_data):
        for column in range(self.table_widget.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row_data[self.keys[column]]))
            self.table_widget.setItem(row_data["user_id"], column, item)

    @pyqtSlot()
    def on_product_button_clicked(self):
        self.product_signal.emit()

    @pyqtSlot()
    def on_update_button_clicked(self):
        self.update_signal.emit()


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = UserView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
