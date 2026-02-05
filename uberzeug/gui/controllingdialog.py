from datetime import date, timedelta
import locale
locale.setlocale(locale.LC_ALL, "")
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from gui.itemlistbox import ItemListbox
from persistence.databasesession import DatabaseSession
from record.logbook import LogBook
from record.logrecord import LogRecord


class ControllingDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, dbsession:DatabaseSession,
                 title:str) -> None:
        self.__dbsession = dbsession
        self.__title = title
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        today: date = date.today()
        first: date = today.replace(day=1)
        prev_month_last_day: date = first - timedelta(days=1)
        prev_month: str = prev_month_last_day.strftime("%m")
        prevmonths_year: str = prev_month_last_day.strftime("%Y")
        yearoptions: List = self.__dbsession.query_distinct_years()
        selected_year: str = prevmonths_year if prevmonths_year in yearoptions\
            else yearoptions[0]
        monthoptions: List = self.__dbsession.\
            query_distinct_months(selected_year)
        selected_month: str = prev_month if prev_month in monthoptions\
            else monthoptions[0]
        projectoptions: List = self.__dbsession.query_distinct_projects(
            selected_year, selected_month)
        
        box = Frame(self)
        yearoption_var: StringVar = StringVar()
        yearoptionmenu: OptionMenu = ttk.OptionMenu(box, yearoption_var,
                                                    *yearoptions)
        yearoption_var.set(selected_year)
        yearoptionmenu.pack(side=LEFT, fill=X, expand=True)
        monthoption_var: StringVar = StringVar()
        monthoptionmenu: OptionMenu = ttk.OptionMenu(box, monthoption_var,
                                                    *monthoptions)
        monthoption_var.set(selected_month)
        monthoptionmenu.pack(side=LEFT, fill=X, expand=True)
        projectoption_var: StringVar = StringVar()
        projectoptionmenu: OptionMenu = ttk.OptionMenu(box, projectoption_var,
                                                    *projectoptions)
        projectoption_var.set(projectoptions[0])
        projectoptionmenu.pack(side=LEFT, fill=X, expand=True)
        box.pack(fill=X, expand=True)
        
        month_of_year: str = f"{yearoption_var.get()}-{monthoption_var.get()}"
        log: sqlite3.Cursor =\
            self.__dbsession.query_log("25_074", month_of_year)
        logbook = LogBook(log)
        self.__listbox = ItemListbox(self, self.__title, logbook.records)
        self.__listbox.set_width(80)
        self.__listbox.pack(padx=5, pady=5)

        box = Frame(self)
        Label(box, text="Kiválasztás összértéke:").pack(side=LEFT,
                                                        expand=True)
        totalvalue_var: IntVar = IntVar()
        totalvalue_var.set(0)
        Label(box, textvariable=totalvalue_var).pack(side=LEFT)
        Label(box, text="Ft").pack()
        box.pack()

    def buttonbox(self):
        """Override standard buttons."""
        box = Frame(self)
        self.__ok_button = ttk.Button(box, text="Export", width=10,
                                      command=self.ok)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Kész", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        box.pack()