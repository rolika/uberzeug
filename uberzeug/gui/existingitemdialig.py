from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from gui.itemlistbox import ItemListbox
from utils.constants import *
from record.stockitemrecord import StockItemRecord


class ExistingItemDialog(simpledialog.Dialog):
    def __init__(self, parent:Widget, title:str, newitem:StockItemRecord,
                 main_list:List[StockItemRecord]) -> None:
        self.__newitem = newitem
        self.__main_list = main_list
        self.__selected_item = None
        super().__init__(parent, title)

    def body(self, parent:Widget) -> Widget:
        self.__itemlistbox = ItemListbox(self, master_list=self.__main_list,
                                         view="valueview")
        self.__itemlistbox.set_width(80)
        self.__itemlistbox.pack(padx=PADX, pady=PADY)
        self.__itemlistbox.bind_selection(self._enable_select_button)
        self.bind_all("<Escape>", self._disable_select_button)
        return self.__itemlistbox.lookup_entry

    def buttonbox(self) -> None:
        box = Frame(self)
        self.__select_button = ttk.Button(box, text="Hozzáadom", width=10,
                                          command=self._existing,
                                          state=DISABLED)
        self.__select_button.pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Új tétel legyen", width=20,
                   command=self._new_item).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Mégse", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def _enable_select_button(self, _:Event=None) -> None:
        self.__select_button["state"] = NORMAL

    def _disable_select_button(self, _:Event=None) -> None:
        self.__select_button["state"] = DISABLED

    def _existing(self, _:Event=None) -> None:
        self.__selected_item = self.__itemlistbox.get_record()
        self.__selected_item.change = self.__newitem.stock
        self.ok()

    def _new_item(self, _:Event=None) -> None:
        self.__selected_item = self.__newitem
        self.ok()

    @property
    def selected_item(self) -> StockItemRecord:
        return self.__selected_item