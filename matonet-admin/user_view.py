# -*- coding: utf-8 -*-
""" user_view.py - presenter for the user table editor"""
__author__ = "topseli"
__license__ = "0BSD"


import os
import sys
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

    def row_count(self):
        return self.table_widget.rowCount()

    def get_row(self, current_row):
        row = {
            "user_id": 0,
            "role": 0,
            "username": "",
            "password": "",
            "is_active": "True",
            "created_at": "",
            "updated_at": ""
        }
        for column in range(self.table_widget.columnCount()):
            item = self.table_widget.item(current_row, column)
            if item is not None and len(item.text()) > 0:
                if column in (0, 1):
                    if int(item.text()) > 0:
                        row[self.keys[column]] = int(item.text())
                    else:
                        raise ValueError
                else:
                    row[self.keys[column]] = item.text()
            else:
                raise ValueError
        return row

    def set_row(self, row_data):
        for column in range(self.table_widget.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row_data[self.keys[column]]))
            self.table_widget.setItem(row_data["user_id"], column, item)


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = UserView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
