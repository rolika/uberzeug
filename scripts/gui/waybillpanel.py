from tkinter import *
from tkinter import ttk
from typing import List

from scripts.rep import Rep
from scripts.stockitemrecord import StockItemRecord


PADX = 2
PADY = 2
TITLE = "Szállítólevél"


class WithdrawPanel(LabelFrame):
    def __init__(self, root=None, title=TITLE, **kwargs) -> None:
        super().__init__(root, text=title, **kwargs)
        Label(self, font=("Liberation Mono", "-12"),
              text=Rep.waybillpanel_header()).pack()
        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X)

    def update_waybill(self, items:List[StockItemRecord]) -> None:
        for widget in self.winfo_children():
            if widget.winfo_class() == "Frame":
                widget.destroy()
        for idx, item in enumerate(items):
            self._add(idx+1, item)

    def _add(self, idx:int, item:StockItemRecord) -> None:
        """The Frame's name corresponds to the item's index in the list."""
        box = Frame(self, name=str(idx))
        Label(box, text=f"{idx:0>4}", font=("Liberation Mono", "-12"))\
            .pack(side=LEFT)
        Label(box, text=item.withdraw_view, font=("Liberation Mono", "-12"))\
            .pack(side=LEFT)
        Button(box, bitmap="error", command=lambda: self._delete_line(box))\
            .pack(padx=PADX, pady=PADY)
        box.pack(anchor=W)

    def _delete_line(self, name:str) -> None:
        self.nametowidget(name).destroy()