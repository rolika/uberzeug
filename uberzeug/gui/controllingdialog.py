import locale

locale.setlocale(locale.LC_ALL, "")

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from gui.itemlistbox import ItemListbox
from record.logrecord import LogRecord


class ControllingDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, log_list:List[LogRecord], title:str) -> None:
        self.__log_list = log_list
        self.__title = title
        super().__init__(root, title=title)
    
    def body(self, root:Widget) -> Widget:
        box = Frame(self)
        self.__listbox = ItemListbox(box, self.__title, self.__log_list)
        self.__listbox.set_width(80)
        self.__listbox.pack(padx=5, pady=5)
        box.pack()
        return self.__listbox