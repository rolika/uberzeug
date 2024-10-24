"""
INVENTORY APPLICATION
"""

import locale
locale.setlocale(locale.LC_ALL, "")

from scripts.gui.askprojectnumber import ask_projectnumber
from scripts.databasesession import DatabaseSession
from scripts.gui.title_ui import TitleUI
from scripts.gui.withdrawdialog import WithdrawDialog


DATABASE = "data/adatok.db"


class InventoryApplication():
    def __init__(self, database:str=DATABASE) -> None:
        self.__dbsession = DatabaseSession(database)
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
        withdraw_dialog = WithdrawDialog(self.__ui, master_list, projectnumber)
        self.__dbsession.log_stock_change(withdraw_dialog.withdraw_list,
                                          projectnumber)



if __name__ == "__main__":
    InventoryApplication()