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
    def refresh_token(self):
        headers = {
                "Authorization": "Bearer %s" % self.tokens["refresh_token"]
            }
        response = requests.post(self.url + "refresh", headers=headers)
        token = json.loads(response.text)
        self.tokens["access_token"] = token["token"]

    def set_products(self, product, row):
            for column in range(self.product_widget.product_table_widget.columnCount()):    
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(product[self.keys[column]]))
                self.product_widget.product_table_widget.setItem(row,column, item)
                

    def get_products(self):
        products = []
        product = {}
        for row in range(self.product_widget.product_table_widget.rowCount()):
            for column in range(self.product_widget.product_table_widget.columnCount()):
                item = self.product_widget.product_table_widget.item(row, column)
                if item is not None and item.text() != "":
                    try:
                        if column in (0,3,5):
                            if int(item.text()) > 0:
                                product[self.keys[column]] = int(item.text())
                            else:
                                raise ValueError
                        if column in (1,2):
                            product[self.keys[column]] = item.text()
                        if column == 6:
                            product[self.keys[column]] = item.text()
                        if column == 7:
                            product[self.keys[column]] = datetime.now().isoformat()
                        if column == 4:
                            if float(item.text()) > 0: 
                                product[self.keys[column]] = float(item.text())
                            else:
                                raise ValueError
                    except ValueError:
                        pass

            if self.product_widget.product_table_widget.item(row, 0) is not None and item.text != "":
                products.append(product)
        return products

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
            self.set_products(product, row)

    def on_update_clicked(self, product_info):
        updated_products = self.get_products()
        self.refresh_token()
        for i in range(len(self.products)):
            try:
                if updated_products[i] != self.products[i]:
                    headers = {
                        "Authorization": "Bearer %s" % self.tokens["access_token"]
                    }
                    try:
                        print(json.dumps(updated_products[i]))
                        requests.patch(self.url + "product/%d" % i,headers=headers, json=json.dumps(updated_products[i]))
                    except requests.Timeout as e:
                        self.product_widget.show_warning(e)
                    return
            except ValueError as e:
                self.product_widget.show_warning(e)
                return
            except TypeError as e:
                self.product_widget.show_warning(e)
                return

def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = MatonetAdmin()
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
