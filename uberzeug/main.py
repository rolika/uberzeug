"""
INVENTORY APPLICATION
"""

import locale
from tkinter import messagebox
from typing import List
locale.setlocale(locale.LC_ALL, "")

from uberzeug._helper.constants import *
from uberzeug._gui.askprojectnumber import ask_projectnumber
from uberzeug._gui.stockitemdialog import stockitem_dialog
from uberzeug._gui.title_ui import TitleUI
from uberzeug._gui.withdrawdialog import withdraw_dialog
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
        self.__ui.mainloop()

    def _bindings(self) -> None:
        self.__ui.withdraw_button = self._withdraw
        self.__ui.takeback_button = self._takeback
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
            messagebox.showinfo(WITHDRAW_TITLE,
                                WAYBILL_TITLE + " száma: " + waybill_number)

    def _takeback(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        takeback_items = withdraw_dialog(self.__ui,
            self.__dbsession.get_project_stock(projectnumber), projectnumber,
            TAKEBACK_TITLE)
        if len(takeback_items):
            for takeback in takeback_items:
                takeback.stock = takeback.backup_stock
                takeback.change = abs(takeback.change)
                takeback.apply_change()
            self.__dbsession.log_stock_change(takeback_items, projectnumber)
            waybill_number = self.__filesession.export_waybill(takeback_items,
                                                               projectnumber)
            messagebox.showinfo(TAKEBACK_TITLE,
                                WAYBILL_TITLE + " száma: " + waybill_number)

    def _newitem(self) -> None:
        newitem = stockitem_dialog(self.__ui, "Új raktári tétel")
        if newitem:
            self.__dbsession.write_item(newitem)


if __name__ == "__main__":
    Uberzeug()