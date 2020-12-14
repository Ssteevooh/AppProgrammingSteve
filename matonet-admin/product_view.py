# -*- coding: utf-8 -*-
""" login_view.py - presenter for the product table editor"""
__author__ = "topseli"
__license__ = "0BSD"

import os
import sys
import requests
from datetime import datetime
from logger import log
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox


class ProductView(QtWidgets.QWidget):

    keys = (
        "product_id",
        "product_name",
        "description",
        "stock",
        "price",
        "size",
        "created_at",
        "updated_at"
    )

    update_signal = pyqtSignal()
    user_signal = pyqtSignal()

    def __init__(self):
        super(ProductView, self).__init__()
        self.init_ui()

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/product_view.ui'
        uic.loadUi(path, self)

    def show_warning(self, e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Invalid values")
        msg.setText("Check the values you entered\n" + str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def row_count(self):
        rows = 0
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 0)
            if item is not None and item.text() != "":
                rows += 1
        return rows

    def get_row(self, current_row):
        row = {
            "product_id": 0,
            "product_name": "",
            "description": "",
            "stock": 0,
            "price": 0.0,
            "size": 0,
            "created_at": "",
            "updated_at": ""
        }
        for column in range(self.table_widget.columnCount()):
            item = self.table_widget.item(current_row, column)
            if item is not None and item.text() != "":
                if column in (0, 3, 5):
                    if int(item.text()) >= 0:
                        row[self.keys[column]] = int(item.text())
                    else:
                        raise ValueError
                if column in (1, 2):
                    row[self.keys[column]] = item.text()
                if column == 4:
                    if float(item.text()) > 0:
                        row[self.keys[column]] = float(item.text())
                    else:
                        raise ValueError
                if column in (6, 7):
                    row[self.keys[column]] = item.text()
            else:
                break
        return row

    def set_row(self, row_data):
        for column in range(self.table_widget.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row_data[self.keys[column]]))
            self.table_widget.setItem(row_data["product_id"], column, item)

    @pyqtSlot()
    def on_users_button_clicked(self):
        self.user_signal.emit()

    @pyqtSlot()
    def on_update_button_clicked(self):
        self.update_signal.emit()


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = ProductView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
