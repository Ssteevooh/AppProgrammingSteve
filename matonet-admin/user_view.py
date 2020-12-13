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

    user_signal = pyqtSignal(int)

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

    @pyqtSlot()
    def on_update_button_clicked(self):

        self.user_signal.emit(1)

    def get_users(self):
        users = []
        user = {}
        for row in range(self.user_table_widget.rowCount()):
            for column in range(self.user_table_widget.columnCount()):
                item = self.user_table_widget.item(row, column)
                if item is not None and item.text() != "":
                    try:
                        if column in (0,3,5):
                            if int(item.text()) >= 0:
                                user[self.keys[column]] = int(item.text())
                            else:
                                raise ValueError
                        if column in (1,2):
                            user[self.keys[column]] = item.text()
                        if column == 4:
                            if float(item.text()) > 0: 
                                user[self.keys[column]] = float(item.text())
                            else:
                                raise ValueError
                        if column in (6,7):
                                user[self.keys[column]] = item.text()    
                    except TypeError as e:
                        self.show_warning(e)
                        return       
                    except ValueError as e:
                        self.show_warning(e)
                        return

            if self.user_table_widget.item(row, 0) is not None and item.text != "":
                users.append(user)
        return users
def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = UserView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
