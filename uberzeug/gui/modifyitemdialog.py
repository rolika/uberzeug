from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from uberzeug.gui.itemlistbox import ItemListbox
from uberzeug._helper.constants import *
from uberzeug.gui.stockitemform import StockItemForm
from uberzeug.record.stockitemrecord import StockItemRecord


class _ModifyItemDialog(simpledialog.Dialog):
    def __init__(self, parent:Widget, title:str,
                 master_list:List[StockItemRecord]):
        self.__master_list = master_list
        self.__modified_item = None
        self.__item_to_modify = None
        super().__init__(parent, title)

    def body(self, parent:Widget) -> ttk.Entry:
        self.__itemlistbox = ItemListbox(self, master_list=self.__master_list)
        self.__itemlistbox.pack(padx=PADX, pady=PADY, side=LEFT)
        self.__itemlistbox.bind_selection(self._populate_form)
        self.__stockitemform = StockItemForm(self)
        self.__stockitemform.pack(padx=PADX, pady=PADY)
        self.bind_all("<Key>", self._check_valid_form)
        return self.__itemlistbox.lookup_entry

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
        self.__modified_item = self.__stockitemform.retrieve()
        self.__modified_item.articlenumber = self.__item_to_modify.articlenumber

    def _populate_form(self, _:Event) -> None:
        self.__item_to_modify = self.__itemlistbox.get_record()
        self.__stockitemform.populate(self.__item_to_modify)
        self._check_valid_form()

    def _check_valid_form(self, _:Event=None) -> None:
        if self.__stockitemform.is_valid():
            self.__ok_button["state"] = NORMAL
        else:
            self.__ok_button["state"] = DISABLED

    @property
    def item(self) -> StockItemRecord:
        return self.__modified_item


def modifyitem_dialog(parent:Widget, master_list:List[StockItemRecord])\
    -> StockItemRecord|None:
    modify = _ModifyItemDialog(parent, MODIFIY_TITLE, master_list)
    modify.unbind_all("<Key>")
    return modify.item