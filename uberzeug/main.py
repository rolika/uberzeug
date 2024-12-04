"""
INVENTORY APPLICATION
"""

import locale
locale.setlocale(locale.LC_ALL, "")
import logging
import socket
from tkinter import messagebox
from typing import List

from uberzeug._helper.constants import *
from uberzeug._gui.asknewexistcancel import ask_newexistcancel
from uberzeug._gui.askprojectnumber import ask_projectnumber
from uberzeug._gui.stockitemdialog import stockitem_dialog
from uberzeug._gui.title_ui import TitleUI
from uberzeug._gui.stockchangedialog\
    import deposit_dialog, takeback_dialog, withdraw_dialog
from uberzeug._persistence.databasesession import DatabaseSession
from uberzeug._persistence.filesession import FileSession


class Uberzeug():
    def __init__(self, title:str=APPLICATION_TITLE,
                 organization:List[str]=ORGANIZATION) -> None:
        self.__dbsession = DatabaseSession()
        self.__filesession = FileSession(organization)
        self.__ui = TitleUI(title, organization, root=self)
        self._bindings()
        self.__ui.pack()
        logging.basicConfig(filename=LOGFILE, encoding='utf-8',
                            format="%(levelname)s: %(asctime)s %(message)s",
                            datefmt="%Y.%m.%d %H:%M:%S", level=logging.INFO)
        self.__ui.mainloop()

    def _bindings(self) -> None:
        self.__ui.withdraw_button = self._withdraw
        self.__ui.takeback_button = self._takeback
        self.__ui.deposit_button = self._desposit
        self.__ui.newitem_button = self._newitem

    def _withdraw(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        master_list = self.__dbsession.load_all_items()
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

    def _desposit(self) -> None:
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


if __name__ == "__main__":
    Uberzeug()