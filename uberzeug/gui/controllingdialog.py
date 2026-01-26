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
        yearoptions: List = [str(year) for year in (2026, 2025, 2024, 2023)]
        yearoption_var: StringVar = StringVar()
        yearoptionmenu: OptionMenu = ttk.OptionMenu(box, yearoption_var,
                                                    *yearoptions)
        yearoption_var.set(yearoptions[0])
        yearoptionmenu.pack(side=LEFT, fill=X, expand=True)
        monthoptions: List = ["január", "február", "itt a nyár"]
        monthoption_var: StringVar = StringVar()
        monthoptionmenu: OptionMenu = ttk.OptionMenu(box, monthoption_var,
                                                    *monthoptions)
        monthoption_var.set(monthoptions[0])
        monthoptionmenu.pack(side=LEFT, fill=X, expand=True)
        box.pack()
        projectoptions: List = ["25/74", "25/399", "26/2"]
        projectoption_var: StringVar = StringVar()
        projectoptionmenu: OptionMenu = ttk.OptionMenu(box, projectoption_var,
                                                    *projectoptions)
        projectoption_var.set(projectoptions[0])
        projectoptionmenu.pack(side=LEFT, fill=X, expand=True)
        box.pack(fill=X, expand=True)
        box = Frame(self)
        self.__listbox = ItemListbox(box, self.__title, self.__log_list)
        self.__listbox.set_width(80)
        self.__listbox.pack(padx=5, pady=5)
        box.pack()
        box = Frame(self)
        Label(box, text="Kiválasztás összértéke:").pack(side=LEFT, expand=True)
        totalvalue_var: IntVar = IntVar()
        totalvalue_var.set(3245678)
        Label(box, textvariable=totalvalue_var).pack(side=LEFT)
        Label(box, text="Ft").pack()
        box.pack()
        return self.__listbox
    
    def buttonbox(self):
        """Override standard buttons."""
        box = Frame(self)
        self.__ok_button = ttk.Button(box, text="Export", width=10,
                                      command=self.ok)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Kész", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        box.pack()