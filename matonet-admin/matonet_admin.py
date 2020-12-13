# -*- coding: utf-8 -*-
__author__ = "topseli"
__license__ = "0BSD"

import sys
import os
import logging
from PyQt5 import QtWidgets, uic
import login_view, product_view, user_view
import requests
import json


class MatonetAdmin(QtWidgets.QWidget):

    products = []

    def __init__(self):
        super(MatonetAdmin, self).__init__()
        self.init_ui()

        # Commented out for instant debugging - We'll use this in production
        """logging.basicConfig(filename='matonet-admin.log',
                            format='%(asctime)s-%(levelname)s:%(message)s',
                            level=logging.DEBUG)"""

        logging.basicConfig(format='%(asctime)s-%(levelname)s:%(message)s',
                            level=logging.DEBUG)

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/main_window.ui'
        uic.loadUi(path, self)

        # Create QWidget instances
        self.login_widget = login_view.LoginView()
        self.product_widget = product_view.ProductView()
        self.user_widget = user_view.UserView()

        # Add QWidget instances to stackedWidget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.product_widget)
        self.stacked_widget.addWidget(self.user_widget)

        # Connect exit_buttons
        self.login_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        self.product_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        self.user_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)

        # Connect signals
        self.login_widget.login_signal.connect(
            self.on_login_clicked)
        self.product_widget.update_signal.connect(
            self.on_update_clicked)
        self.product_widget.user_signal.connect(
            self.on_user_clicked)

    def login(self, login_info):
        try:
            self.url = "http://" + login_info["address"] + ":5000/"
            print(login_info)
            response = requests.post(self.url + "token", json={
                "username": login_info["username"], "password": login_info["password"]}, timeout=2)
            self.tokens = json.loads(response.text)
        except Exception:
            pass

    def logout(self):
        headers = {"Authorization": "Bearer %s" % self.tokens["access_token"]}
        requests.post(self.url + "revoke", json={}, headers=headers)

    def fetch_from_db(self, endpoint):
        try:
            self.refresh_token()
            headers = {"Authorization": "Bearer %s" % self.tokens["access_token"]}
            return requests.get(self.url + endpoint, headers=headers)
        except Exception:
            pass

    def refresh_token(self):
        headers = {"Authorization": "Bearer %s" % self.tokens["refresh_token"]}
        response = requests.post(self.url + "refresh", headers=headers)
        token = json.loads(response.text)
        self.tokens["access_token"] = token["token"]

    def on_exit_button_clicked(self):
        if self.stacked_widget.currentWidget() is not self.login_widget:
            self.logout()
            logging.info("User %s logged out." % self.user)
        sys.exit(0)

    def on_login_clicked(self, login_info):
        self.login(login_info)
        self.user = login_info["username"]
        try:
            product_db = self.fetch_from_db("products")
            self.products = json.loads(product_db.text)
        except requests.ConnectionError as e:
            self.login_widget.show_warning(e)
            return
        except requests.Timeout as e:
            self.login_widget.show_warning(e)
            return
        except AttributeError as e:
            self.login_widget.show_warning(e)
            return

        logging.info("User %s logged in." % self.user)
        self.stacked_widget.setCurrentWidget(self.product_widget)
        logging.info("User %s is viewing products." % self.user)
        for row, product in enumerate(self.products):
            self.product_widget.set_products(product, row)

    def on_update_clicked(self):
        if self.stacked_widget.currentWidget() is self.product_widget:
            self.refresh_token()
            self.product_widget.update_products(self.products, self.url, self.tokens["access_token"])
            logging.info("products updated by %s" % self.login_info["username"])

    def on_user_clicked(self, int):
        try:
            user_db = self.fetch_from_db("users")
            self.users = json.loads(user_db.text)
        except requests.ConnectionError as e:
            self.login_widget.show_warning(e)
            return
        except requests.Timeout as e:
            self.login_widget.show_warning(e)
            return
        self.stacked_widget.setCurrentWidget(self.user_widget)
        logging.info("User %s is viewing users." % self.user)
        for row, user in enumerate(self.users):
            self.user_widget.set_users(user, row)

def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = MatonetAdmin()
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
