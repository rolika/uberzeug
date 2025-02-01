from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from utils.constants import *
from gui.stockitemform import StockItemForm
from record.stockitemrecord import StockItemRecord


class _StockItemDialog(simpledialog.Dialog):
    def __init__(self, parent:Widget, title:str) -> None:
        self.__stockitem = None
        super().__init__(parent, title)

    def body(self, parent:Widget) -> Widget:
        self.__stockitemform = StockItemForm(self)
        self.__stockitemform.pack()
        self.bind_all("<Key>", self._is_stockitem_valid)
        return self.__stockitemform.name_entry

    def buttonbox(self):
        """Override standard buttons."""
        box = Frame(self)
        self.__ok_button = ttk.Button(box, text="KÉSZ", width=10,
                                      command=self.ok, state=DISABLED)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Mégse", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        box.pack()
    
    def apply(self) -> None:
        if self.__stockitemform.is_valid():
            self.__stockitem = self.__stockitemform.retrieve()
    
    def get(self) -> StockItemRecord|None:
        return self.__stockitem

    def _is_stockitem_valid(self, _:Event) -> None:
        if self.__stockitemform.is_valid():
            self.__ok_button["state"] = NORMAL
        else:
            self.__ok_button["state"] = DISABLED


def stockitem_dialog(parent:Widget, title:str) -> StockItemRecord|None:
    stockitem = _StockItemDialog(parent, title)
    stockitem.unbind_all("<Key>")
    return stockitem.get()