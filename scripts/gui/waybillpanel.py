from tkinter import *
from tkinter import ttk
from typing import List

from scripts.stockitemrecord import StockItemRecord


TITLE = "Szállítólevél"

class WithdrawPanel(LabelFrame):
    def __init__(self, root=None, title=TITLE, **kwargs) -> None:
        super().__init__(root, text=title, **kwargs)
    
    def add(self, item:StockItemRecord) -> None:
        box = Frame(self)
        Label(box, text="ssz", font=("Liberation Mono", "-12")).pack(side=LEFT)
        Label(box, text=item.withdraw_view, font=("Liberation Mono", "-12")).pack(side=LEFT)
        Button(box, bitmap="error", command=lambda: self._delete_line(box)).pack()
        box.pack()
    
    def _delete_line(self, box:Frame) -> None:
        box.destroy()