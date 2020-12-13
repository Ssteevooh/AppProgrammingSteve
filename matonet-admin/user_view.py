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

    update_signal = pyqtSignal(list)
    product_signal = pyqtSignal(int)

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

    def delete_uneditables(self, user):
        user.pop("user_id", None)
        user.pop("role", None)
        user.pop("created_at", None)
        user.pop("updated_at", None)
        return user

    def set_users(self, user, row):
        for column in range(self.user_table_widget.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(user[self.keys[column]]))
            self.user_table_widget.setItem(row, column, item)

    def update_users(self, username, users, url, token):
        updated_users = self.get_users()
        for i in range(len(users)):
            try:
                if updated_users[i] != users[i]:
                    updated_json = self.delete_uneditables(updated_users[i])
                    headers = {"Authorization": "Bearer %s" % token}
                    print(updated_json)
                    response = requests.patch(url + "user/%d" % i, headers=headers, json=updated_json)
                    if response.status_code == 200:
                        log.info("Users updated by %s" % username)
                    else:
                        log.error("Failed to update user %s" % username)
            except requests.Timeout as e:
                self.show_warning(e)
                return
            except ValueError as e:
                self.show_warning(e)
                return
            except TypeError as e:
                self.show_warning(e)
                return

    def get_users(self):
        users = []
        user = {}
        for row in range(self.user_table_widget.rowCount()):
            for column in range(self.user_table_widget.columnCount()):
                item = self.user_table_widget.item(row, column)
                if item is not None and item.text() != "":
                    try:
                        if column in (0, 1):
                            if int(item.text()) >= 0:
                                user[self.keys[column]] = int(item.text())
                            else:
                                raise ValueError
                        if column in (2, 3):
                            user[self.keys[column]] = item.text()
                        if column == 4:
                            user[self.keys[column]] = item.text()
                        if column in (5, 6):
                            user[self.keys[column]] = item.text()
                    except KeyError as e:
                        self.show_warning(e)
                        return
                    except TypeError as e:
                        self.show_warning(e)
                        return
                    except ValueError as e:
                        self.show_warning(e)
                        return

            if self.user_table_widget.item(row, 0) is not None and item.text != "":
                users.append(user)
        return users

    @pyqtSlot()
    def on_product_button_clicked(self):
        self.product_signal.emit(1)

    @pyqtSlot()
    def on_update_button_clicked(self):
        users = self.get_users()
        self.update_signal.emit(users)


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = UserView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
