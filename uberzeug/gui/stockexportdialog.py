import locale
locale.setlocale(locale.LC_ALL, "")
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from gui.itemlistbox import ItemListbox
from record.stockitemrecord import StockItemRecord


class StockExportDialog(simpledialog.Dialog):
    def __init__(self, parent:Widget, title:str, master_list:List) -> None:
        self.__master_list = master_list
        self.__title = title
        self.__selected_records:List[StockItemRecord] = []
        self.__lookup_term:str = ""
        super().__init__(parent, title)

    def body(self, parent:Widget) -> Widget:
        self.__totalvalue_var: IntVar = IntVar()
        self.__itemlistbox = ItemListbox(self, self.__title, self.__master_list,
                                         self._lookup_callback, "valueview")
        self.__itemlistbox.set_width(80)
        self.__itemlistbox.pack(padx=5, pady=5)
        box = Frame(self)
        Label(box, text="Kiválasztás összértéke:").pack(side=LEFT,
                                                        expand=True)
        self.__totalvalue_var.set(0)
        Label(box, textvariable=self.__totalvalue_var).pack(side=LEFT)
        Label(box, text="Ft").pack()
        box.pack()
        self._lookup_callback(self.__itemlistbox.display_list)
        return self.__itemlistbox.lookup_entry

    def buttonbox(self):
        """Override standard buttons."""
        box = Frame(self)
        ttk.Button(box, text="Export", width=10,
                   command=self.ok).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Mégse", width=10,
                   command=self.cancel).pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def apply(self) -> None:
        self.__lookup_term = self.__itemlistbox.lookup_entry.get()
        self.__selected_records = self.__itemlistbox.display_list

    @property
    def selected_records(self) -> List[StockItemRecord]:
        return self.__selected_records

    @property
    def total_value(self) -> float:
        return sum(item.value for item in self.__itemlistbox.display_list)

    @property
    def lookup_term(self) -> str:
        return self.__lookup_term

    def _lookup_callback(self, selection:List[StockItemRecord]) -> None:
        total = sum(record.value for record in selection)
        self.__totalvalue_var.set(\
            locale.format_string("%+.2f", total, grouping=True))