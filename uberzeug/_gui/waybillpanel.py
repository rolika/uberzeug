from tkinter import *
from tkinter import ttk
from typing import List

from uberzeug._gui.itemlistbox import ItemListbox
import uberzeug._helper.textrep as textrep
from uberzeug._record.stockitemrecord import StockItemRecord


PADX = 2
PADY = 2
TITLE = "Szállítólevél"


class WaybillPanel(LabelFrame):
    def __init__(self, root=None, title=TITLE,
                 temp_list:List[StockItemRecord]=[],
                 itemlistbox:ItemListbox=None, **kwargs) -> None:
        super().__init__(root, text=title, **kwargs)
        self.__temp_list = temp_list
        self.__itemlistbox = itemlistbox
        Label(self, font=("Liberation Mono", "-12"),
              text=textrep.waybillpanel_header()).pack()
        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X)
        self.__box = Frame(self)
        self.__box.pack(expand=True, fill=X, anchor=W)

    def update_waybill(self) -> None:
        for line in self.__box.winfo_children():
            line.destroy()
        for idx, item in enumerate(self.__temp_list):
            self._add_line(idx + 1, item)

    def _add_line(self, idx:int, item:StockItemRecord) -> None:
        """The Frame's name corresponds to the item's index in the list."""
        line = Frame(self.__box, name=str(idx))
        Label(line, text=f"{idx:0>4}", font=("Liberation Mono", "-12"))\
            .pack(side=LEFT)
        Label(line, text=item.withdraw_view, font=("Liberation Mono", "-12"))\
            .pack(side=LEFT)
        Button(line, bitmap="error",
               command=lambda: self._undo(line.winfo_name()))\
            .pack(padx=PADX, pady=PADY)
        line.pack(expand=True, fill=X, anchor=W)

    def _undo(self, name:str) -> None:
        idx = int(name) - 1
        item = self.__temp_list.pop(idx)
        item.undo_change()
        self.__itemlistbox.update_item(item)
        self.update_waybill()