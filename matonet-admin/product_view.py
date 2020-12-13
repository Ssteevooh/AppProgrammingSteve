# -*- coding: utf-8 -*-
""" login_view.py - presenter for the product table editor"""
__author__ = "topseli"
__license__ = "0BSD"


import os
import sys
import requests
import json
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

    user_signal = pyqtSignal(int)
    update_signal = pyqtSignal(list)

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

    def delete_uneditables(self, product):
        product.pop("product_id", None)
        product.pop("created_at", None)
        product.pop("updated_at", None)
        return product

    def set_products(self, product, row):
            for column in range(self.product_table_widget.columnCount()):    
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(product[self.keys[column]]))
                self.product_table_widget.setItem(row,column, item)
                

    def get_products(self):
        products = []
        product = {}
        for row in range(self.product_table_widget.rowCount()):
            for column in range(self.product_table_widget.columnCount()):
                item = self.product_table_widget.item(row, column)
                if item is not None and item.text() != "":
                    try:
                        if column in (0,3,5):
                            if int(item.text()) >= 0:
                                product[self.keys[column]] = int(item.text())
                            else:
                                raise ValueError
                        if column in (1,2):
                            product[self.keys[column]] = item.text()
                        if column == 4:
                            if float(item.text()) > 0: 
                                product[self.keys[column]] = float(item.text())
                            else:
                                raise ValueError
                        if column in (6,7):
                                product[self.keys[column]] = item.text()    
                    except TypeError as e:
                        self.show_warning(e)
                        return       
                    except ValueError as e:
                        self.show_warning(e)
                        return

            if self.product_table_widget.item(row, 0) is not None and item.text != "":
                products.append(product)
        return products

    def update_products(self, products, url, token):
        updated_products = self.get_products()
        for i in range(len(products)):
            try:
                if updated_products[i] != products[i]:
                    updated_json = self.delete_uneditables(updated_products[i])
                    print(updated_json)
                headers = {
                "Authorization": "Bearer %s" % token
                }
                try:
                    requests.patch(url + "product/%d" % i, headers=headers, json=updated_json)
                except requests.Timeout as e:
                    self.show_warning(e)
                    pass
                except ValueError as e:
                    self.show_warning(e)
                    pass
                except TypeError as e:
                    self.show_warning(e)
                    pass

            except Exception as e:
                self.show_warning(e)
            
    @pyqtSlot()
    def on_users_button_clicked(self):
        self.user_signal.emit(1)

    @pyqtSlot()
    def on_update_button_clicked(self):
        products = self.get_products()
        self.update_signal.emit(products)


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = ProductView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
