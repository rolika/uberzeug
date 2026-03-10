from datetime import date
import locale

locale.setlocale(locale.LC_ALL, "")
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from gui.itemlistbox import ItemListbox
from utils.constants import *
from record.stockitemrecord import StockItemRecord


class ShortageWarningDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, title:str, lookback_days:int,
                 shortitems:List[StockItemRecord]) -> None:
        self.__lookback_days = lookback_days
        self.__shortitems = shortitems
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        box = Frame(self)
        Label(box, text=f"Az elmúlt {self.__lookback_days} napban a következő\n"
            "cikkekből fogyás volt, és a szállítási idejüket is figyelembe\n"
            "véve elképzelhető, hogy a készlet nem lesz elegendő.")\
            .pack(padx=PADX, pady=PADY)
        self.__itemlistbox = ItemListbox(box, title="Rövidülő cikkek",
                                         master_list=self.__shortitems,
                                         view="deliveryview")
        self.__itemlistbox.set_width(80)
        self.__itemlistbox.pack(padx=PADX, pady=PADY)
        box.pack(padx=PADX, pady=PADY)
        return box

    def buttonbox(self):
        """Override standard buttons."""
        box = Frame(self)
        self.__ok_button = ttk.Button(box, text="Export", width=10,
                                      command=self.ok)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Kész", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        box.pack()
    
    def apply(self):
        return super().apply()