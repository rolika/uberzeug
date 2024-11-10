"""
INVENTORY APPLICATION
"""

import locale
locale.setlocale(locale.LC_ALL, "")

from uberzeug._persistence.filesession import FileSession
from uberzeug._gui.askprojectnumber import ask_projectnumber
from uberzeug._persistence.databasesession import DatabaseSession
from uberzeug._gui.title_ui import TitleUI
from uberzeug._gui.withdrawdialog import withdraw_dialog


class Uberzeug():
    def __init__(self) -> None:
        self.__dbsession = DatabaseSession()
        self.__filesession = FileSession()
        self.__ui = TitleUI(self)
        self._bindings()
        self.__ui.pack()
        self.__ui.mainloop()

    def _bindings(self) -> None:
        self.__ui.withdraw_button= self._withdraw

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


if __name__ == "__main__":
    Uberzeug()