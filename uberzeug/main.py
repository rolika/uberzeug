"""
INVENTORY APPLICATION
"""

import locale
from typing import List
locale.setlocale(locale.LC_ALL, "")

from uberzeug._helper.constants import *
from uberzeug._gui.askprojectnumber import ask_projectnumber
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

    def _withdraw(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        master_list = self.__dbsession.load_all_items()
        withdrawed_items = withdraw_dialog(self.__ui, master_list,
                                           projectnumber)
        if len(withdrawed_items):
            self.__dbsession.log_stock_change(withdrawed_items, projectnumber)
            self.__filesession.export_waybill(withdrawed_items, projectnumber)

    def _takeback(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return


if __name__ == "__main__":
    Uberzeug()