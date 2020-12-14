# -*- coding: utf-8 -*-
__author__ = "topseli"
__license__ = "0BSD"

import sys
import os
from logger import log
from PyQt5 import QtWidgets, uic
import login_view, product_view, user_view, add_user_view
import requests


class MatonetAdmin(QtWidgets.QWidget):

    product_keys = (
        "product_id",
        "product_name",
        "description",
        "stock",
        "price",
        "size",
        "created_at",
        "updated_at"
    )

    user_keys = (
        "user_id",
        "role",
        "username",
        "password",
        "is_active",
        "created_at",
        "updated_at"
    )

    def __init__(self):
        super(MatonetAdmin, self).__init__()
        self.init_ui()

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/main_window.ui'
        uic.loadUi(path, self)

        # Create QWidget instances
        self.login_widget = login_view.LoginView()
        self.product_widget = product_view.ProductView()
        self.user_widget = user_view.UserView()
        self.add_user_widget = add_user_view.AddUserView()

        # Add QWidget instances to stackedWidget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.product_widget)
        self.stacked_widget.addWidget(self.user_widget)
        self.stacked_widget.addWidget(self.add_user_widget)

        # Connect exit_buttons
        self.login_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        self.product_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        self.user_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        self.add_user_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        # Connect signals
        self.login_widget.login_signal.connect(
            self.on_login_clicked)
        self.product_widget.users_button.clicked.connect(
            self.on_user_clicked)
        self.product_widget.update_button.clicked.connect(
            self.on_update_clicked)
        self.user_widget.product_button.clicked.connect(
            self.on_product_clicked)
        self.user_widget.add_button.clicked.connect(
            self.on_add_button_clicked)
        self.user_widget.update_button.clicked.connect(
            self.on_update_clicked)
        self.add_user_widget.create_user_button_signal.connect(
            self.create_user)

    def delete_static_fields(self, row):
        if self.stacked_widget.currentWidget() is self.product_widget:
            row.pop("product_id", None)
        if self.stacked_widget.currentWidget() is self.user_widget:
            row.pop("user_id", None)

        row.pop("created_at", None)
        row.pop("updated_at", None)

    def login(self, login_info):
        try:
            self.login_info = login_info
            self.url = "http://" + login_info["address"] + ":5000/"
            response = requests.post(self.url + "token", json={
                "username": login_info["username"], "password": login_info["password"]}, timeout=2)
            log.info(response.status_code)
            self.tokens = response.json()
        except Exception:
            pass

    def create_user(self, user_info):
        print(user_info)
        try:
            headers = {"Authorization": "Bearer %s" % self.tokens["refresh_token"]}
            response = requests.post(self.url + "users", json={
                "username": user_info["username"], "password": user_info["password"]}, headers=headers, timeout=2)
            log.info(response.status_code)
        except Exception:
            pass

    def refresh_token(self):
        headers = {"Authorization": "Bearer %s" % self.tokens["refresh_token"]}
        response = requests.post(self.url + "refresh", headers=headers)
        if response.status_code == 200:
            token = response.json()
            log.info(response.status_code)
            self.tokens["access_token"] = token["token"]

    def logout(self):
        headers = {"Authorization": "Bearer %s" % self.tokens["access_token"]}
        requests.post(self.url + "revoke", json={}, headers=headers)

    def fetch_from_db(self, endpoint):
        headers = {"Authorization": "Bearer %s" % self.tokens["access_token"]}
        response = requests.get(self.url + endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            self.refresh_token()
            response = requests.get(self.url + endpoint, headers=headers)
            log.info(response.status_code)
            return response.json()

    def check_changes(self):
        if self.stacked_widget.currentWidget() is self.product_widget:
            endpoint = "product"
        if self.stacked_widget.currentWidget() is self.user_widget:
            endpoint = "user"

        ui_data = []
        for row in range(self.stacked_widget.currentWidget().row_count()):

            try:
                row_data = self.stacked_widget.currentWidget().get_row(row)
                db_data = self.fetch_from_db(endpoint + "/%s" % (row_data[endpoint + "_id"]))
            except ValueError:
                row_data = None
            if row_data is not None:
                for key in row_data.keys():
                    if db_data[0][key] != row_data[key]:
                        ui_data.append(row_data)

        return ui_data

    def load_table(self):
        if self.stacked_widget.currentWidget() is self.product_widget:
            table = "products"
        if self.stacked_widget.currentWidget() is self.user_widget:
            table = "users"
        db_data = self.fetch_from_db(table)
        log.info("User %s is viewing %s." % (self.user, table))
        for row in db_data:
            self.stacked_widget.currentWidget().set_row(row)

    def update_db(self, rows_to_update):
        for row in range(len(rows_to_update)):
            if self.stacked_widget.currentWidget() is self.product_widget:
                endpoint = "product"
                index = int(rows_to_update[row]["product_id"])
            if self.stacked_widget.currentWidget() is self.user_widget:
                endpoint = "user"
                try:
                    index = int(rows_to_update[row]["user_id"])
                # TODO Find out why KeyError is occurring
                except KeyError:
                    return
            self.delete_static_fields(rows_to_update[row])
            headers = {"Authorization": "Bearer %s" % self.tokens["access_token"]}
            response = requests.patch(self.url + endpoint + "/%d" % index, headers=headers,
                                      json=rows_to_update[row])
            if response.status_code == 200:
                log.info("User %s updated %s %s" % (self.user, endpoint, str(index)))

    def on_exit_button_clicked(self):
        if self.stacked_widget.currentWidget() is not self.login_widget:
            self.logout()
            log.info("User %s logged out." % self.user)
        sys.exit(0)

    def on_login_clicked(self, login_info):
        self.login(login_info)
        self.user = login_info["username"]
        log.info("User %s logged in." % self.user)
        self.stacked_widget.setCurrentWidget(self.product_widget)
        self.load_table()

    def on_update_clicked(self):
        changed_rows = self.check_changes()
        if changed_rows:
            self.update_db(changed_rows)
            changed_rows = None
        else:
            log.info("Nothing to update")

    def on_product_clicked(self):
        self.product_db = self.fetch_from_db("products")
        self.stacked_widget.setCurrentWidget(self.product_widget)
        self.load_table()

    def on_user_clicked(self):
        self.user_db = self.fetch_from_db("users")
        self.stacked_widget.setCurrentWidget(self.user_widget)
        self.load_table()

    def on_add_button_clicked(self):
        if self.stacked_widget.currentWidget() is self.product_widget:
            return
        if self.stacked_widget.currentWidget() is self.user_widget:
            self.stacked_widget.setCurrentWidget(self.add_user_widget)


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = MatonetAdmin()
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()
