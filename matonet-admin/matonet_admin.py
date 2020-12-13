# -*- coding: utf-8 -*-
__author__ = "topseli"
__license__ = "0BSD"

import sys
import os
import logging
from PyQt5 import QtWidgets, uic
import login_view, product_view
import requests
import json
import site
from datetime import datetime

class MatonetAdmin(QtWidgets.QWidget):

    products = []

    def __init__(self):
        super(MatonetAdmin, self).__init__()
        self.init_ui()
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/main_window.ui'
        uic.loadUi(path, self)

        # Create QWidget instances
        self.login_widget = login_view.LoginView()
        self.product_widget = product_view.ProductView()
        
        # Add QWidget instances to stackedWidget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.product_widget)


        # Connect exit_buttons
        self.login_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        
        self.product_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)

        # Connect signals
        self.login_widget.login_signal.connect(
            self.on_login_clicked)
        self.product_widget.update_signal.connect(
            self.on_update_clicked)

    def refresh_token(self):
        headers = {
                "Authorization": "Bearer %s" % self.tokens["refresh_token"]
            }
        response = requests.post(self.url + "refresh", headers=headers)
        token = json.loads(response.text)
        self.tokens["access_token"] = token["token"]

    def on_exit_button_clicked(self):
        sys.exit(0)

    def on_login_clicked(self, login_info):
        self.url = "http://" + login_info["address"] + ":5000/"
        
        try:
            response = requests.post(self.url + "token", json={
                "username": login_info["username"], "password": login_info["username"]}, timeout=2)
            self.tokens = json.loads(response.text)
            headers = {
                "Authorization": "Bearer %s" % self.tokens["access_token"]
            }
            db = requests.get(self.url + "products", headers=headers)
            self.products = json.loads(db.text)
        except requests.Timeout as e:
            self.login_widget.show_warning(e)
            return

        self.stacked_widget.setCurrentWidget(self.product_widget)
        
        for row, product in enumerate(self.products):
            self.product_widget.set_products(product, row)
    
    def on_update_clicked(self):
        if self.stacked_widget.currentWidget() is self.product_widget:
            self.refresh_token()
            self.product_widget.update_products(self.products, self.url, self.tokens["access_token"])


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = MatonetAdmin()
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
