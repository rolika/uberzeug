"""
ÜBERZEUG
"""


import configparser
import locale
locale.setlocale(locale.LC_ALL, "")
import logging
import socket
from tkinter import messagebox
from typing import List

from uberzeug._helper.constants import *
from uberzeug._gui.asknewexistcancel import ask_newexistcancel
from uberzeug._gui.askprojectnumber import ask_projectnumber
from uberzeug._gui.modifyitemdialog import modifyitem_dialog
from uberzeug._gui.stockitemdialog import stockitem_dialog
from uberzeug._gui.title_ui import TitleUI
from uberzeug._gui.stockchangedialog\
    import delete_dialog, deposit_dialog, takeback_dialog, withdraw_dialog
from uberzeug._persistence.databasesession import DatabaseSession
from uberzeug._persistence.filesession import FileSession


class Uberzeug():
    def __init__(self, title:str=APPLICATION_TITLE,
                 organization:List[str]=ORGANIZATION) -> None:

        config = configparser.ConfigParser()
        config.read(CONFIGFILE)
        database_file = config["DEFAULT"]["database"]
        waybillfolder = config["DEFAULT"]["waybillfolder"]
        logfile = config["DEFAULT"]["logfile"]
        title_image = config["DEFAULT"]["title_image"]
        windows_icon = config["DEFAULT"]["windows_icon"]
        linux_icon = config["DEFAULT"]["linux_icon"]

        self.__dbsession = DatabaseSession(database_file)
        self.__filesession = FileSession(organization, waybillfolder)
        self.__ui = TitleUI(title, organization, title_image, windows_icon,
                            linux_icon, root=self)
        self._bindings()
        self._update_buttons()
        self.__ui.pack()
        logging.basicConfig(filename=logfile, encoding='utf-8',
                            format="%(levelname)s: %(asctime)s %(message)s",
                            datefmt="%Y.%m.%d %H:%M:%S", level=logging.INFO)
        self.__ui.mainloop()

    def _bindings(self) -> None:
        self.__ui.withdraw_button = self._withdraw
        self.__ui.takeback_button = self._takeback
        self.__ui.deposit_button = self._deposit
        self.__ui.newitem_button = self._newitem
        self.__ui.modify_button = self._modify
        self.__ui.delete_button = self._delete

    def _withdraw(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        master_list = self.__dbsession.load_withdrawable_items()
        withdrawed_items = withdraw_dialog(self.__ui, master_list,
                                           projectnumber)
        if len(withdrawed_items):
            self.__dbsession.log_stock_change(withdrawed_items, projectnumber)
            waybill_number = self.__filesession.export_waybill(withdrawed_items,
                                                               projectnumber)
            logging.info(f"{socket.gethostname()} withdraw: {waybill_number}")
            messagebox.showinfo(WITHDRAW_TITLE,
                                WAYBILL_TITLE + " száma: " + waybill_number)

    def _takeback(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        master_list = self.__dbsession.get_project_stock(projectnumber)
        takeback_items = takeback_dialog(self.__ui, master_list, projectnumber)
        if len(takeback_items):
            for takeback in takeback_items:
                takeback.stock = takeback.backup_stock
                takeback.change = abs(takeback.change)
                takeback.apply_change()
            self.__dbsession.log_stock_change(takeback_items, projectnumber)
            waybill_number = self.__filesession.export_waybill(takeback_items,
                                                               projectnumber)
            logging.info(f"{socket.gethostname()} takeback: {waybill_number}")
            messagebox.showinfo(TAKEBACK_TITLE,
                                WAYBILL_TITLE + " száma: " + waybill_number)

    def _deposit(self) -> None:
        master_list = self.__dbsession.load_all_items()
        deposit_items = deposit_dialog(self.__ui, master_list)
        pieces = len(deposit_items)
        if pieces:
            self.__dbsession.update_stock(deposit_items)
            logging.info(f"{socket.gethostname()} deposit: {pieces} items")
            messagebox.showinfo(DEPOSIT_TITLE, f"{pieces} tétel bevételezve.")

    def _newitem(self) -> None:
        newitem = stockitem_dialog(self.__ui, "Új raktári tétel")
        host = socket.gethostname()
        if newitem:
            log = f"new: {newitem.name} {newitem.stock}"
            message = f"új anyag: {newitem.name} {newitem.stock} {newitem.unit}"
            existing_stockitem = self.__dbsession.lookup(newitem)
            if existing_stockitem:
                answer = ask_newexistcancel(self.__ui)
                if answer == "new":
                    self.__dbsession.insert(newitem)
                elif answer == "exist":
                    setattr(existing_stockitem, "change", newitem.stock)
                    existing_stockitem.apply_change()
                    self.__dbsession.update(existing_stockitem)
                    log = f"update: {newitem.name} +{newitem.stock}"
            else:
                self.__dbsession.insert(newitem)
            logging.info(f"{host} {log}")
            messagebox.showinfo("Felvéve a raktárba", message)
        self._update_buttons()

    def _modify(self) -> None:
        master_list = self.__dbsession.load_all_items()
        item = modifyitem_dialog(self.__ui, master_list)
        if item:
            self.__dbsession.update(item)
            logging.info\
                (f"{socket.gethostname()} modify: {item.name} {item.stock}")
            messagebox.showinfo(MODIFIY_TITLE,
                f"{item.name} {item.stock} {item.unit}")

    def _delete(self) -> None:
        master_list = self.__dbsession.load_all_items()
        items = delete_dialog(self.__ui, master_list)
        if len(items) and\
            messagebox.askokcancel(DELETE_TITLE, "Biztos vagy benne?"):
            for item in items:
                self.__dbsession.delete(item)
                logging.info\
                    (f"{socket.gethostname()} delete: {item.name} {-item.change}")
            messagebox.showinfo(DELETE_TITLE, "Anyag(ok) törölve.")
        self._update_buttons()

    def _update_buttons(self) -> None:
        empty_db = not len(self.__dbsession.load_all_items())
        self.__ui.switch_button_state(empty_db)


if __name__ == "__main__":
    Uberzeug()