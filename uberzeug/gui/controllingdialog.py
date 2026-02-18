from datetime import datetime, date, timedelta
import locale
locale.setlocale(locale.LC_ALL, "")
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from gui.itemlistbox import ItemListbox
from persistence.databasesession import DatabaseSession
from persistence.filesession import FileSession
from record.logbook import LogBook
from record.logrecord import LogRecord
from utils.projectnumber import Projectnumber


class ControllingDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, dbsession:DatabaseSession,
                 filesession:FileSession, title:str) -> None:
        self.__dbsession = dbsession
        self.__filesession = filesession
        self.__title = title
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        today: date = date.today()
        first: date = today.replace(day=1)
        prev_month_last_day: date = first - timedelta(days=1)
        self.__prev_month: str = prev_month_last_day.strftime("%B")

        box = Frame(self)
        prevmonths_year: str = prev_month_last_day.strftime("%Y")
        yearoptions: List = self.__dbsession.query_distinct_years()
        selected_year: str = prevmonths_year if prevmonths_year in yearoptions\
            else yearoptions[0]
        self.__yearoption_var: StringVar = StringVar()
        yearoptionmenu: OptionMenu = OptionMenu(
            box, self.__yearoption_var, *yearoptions)
        self.__yearoption_var.set(selected_year)
        self.__yearoption_var.trace("w", self._update_months)
        yearoptionmenu.pack(side=LEFT, fill=X, expand=True)

        self.__monthoption_var: StringVar = StringVar()
        self.__monthoptionmenu: OptionMenu = OptionMenu(
            box, self.__monthoption_var, "")
        self.__monthoption_var.trace("w", self._update_projects)
        self.__monthoptionmenu.pack(side=LEFT, fill=X, expand=True)

        self.__projectoption_var: StringVar = StringVar()
        self.__projectoptionmenu: OptionMenu = OptionMenu(
            box, self.__projectoption_var, "")
        self.__projectoption_var.trace("w", self._update_log)
        self.__projectoptionmenu.pack(side=LEFT, fill=X, expand=True)
        box.pack(fill=X, expand=True)

        self.__totalvalue_var: IntVar = IntVar()  # declare before itemlistbox
        month_of_year: str =\
            f"{self.__yearoption_var.get()}-{self.__monthoption_var.get()}"
        project: str = self.__projectoption_var.get()
        log: sqlite3.Cursor =\
            self.__dbsession.query_log(project, month_of_year)
        logbook = LogBook(log)
        self.__listbox = ItemListbox(self, self.__title, logbook.records,
                                     self._lookup_callback)
        self.__listbox.set_width(80)
        self.__listbox.pack(padx=5, pady=5)

        box = Frame(self)
        Label(box, text="Kiválasztás összértéke:").pack(side=LEFT,
                                                        expand=True)
        self.__totalvalue_var.set(0)
        Label(box, textvariable=self.__totalvalue_var).pack(side=LEFT)
        Label(box, text="Ft").pack()
        box.pack()
        self._lookup_callback(logbook.records)

        self._update_months()
        self._update_projects()

    def buttonbox(self):
        """Override standard buttons."""
        box = Frame(self)
        self.__ok_button = ttk.Button(box, text="Export", width=10,
                                      command=self.ok)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text="Kész", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def apply(self) -> None:
        selected_year = self.__yearoption_var.get()
        selected_month = self.__monthoption_var.get()
        selected_month = datetime.strptime(selected_month, "%B").strftime("%m")
        selected_project = self.__projectoption_var.get()
        log:List[LogRecord] = self.__listbox.display_list
        logbook = LogBook.from_records(log)
        self.__filesession.export_turnover(
            projectnumber=Projectnumber(selected_project),
            yearmonth=date(int(selected_year), int(selected_month), 1),
            items=logbook.records,
            total=sum(record.value for record in logbook.records),
            lookup_term=self.__listbox.lookup_entry.get())

    def _update_months(self, *args) -> None:
        self.__listbox.clear_selection()
        selected_year = self.__yearoption_var.get()
        monthoptions = [date(1900, int(month), 1).strftime("%B")\
                            for month in self.__dbsession.\
                                query_distinct_months(selected_year)]
        menu = self.__monthoptionmenu["menu"]
        menu.delete(0, "end")
        for month in monthoptions:
            menu.add_command(label=month, command=lambda value=month:\
                    self.__monthoptionmenu.setvar(\
                        self.__monthoptionmenu.cget("textvariable"), value))
        if monthoptions:
            month: str = self.__prev_month\
                if self.__prev_month in monthoptions else monthoptions[0]
            self.__monthoptionmenu.setvar(\
                self.__monthoptionmenu.cget("textvariable"), month)
        self._update_projects()

    def _update_projects(self, *args) -> None:
        self.__listbox.clear_selection()
        selected_year = self.__yearoption_var.get()
        selected_month = self.__monthoption_var.get()
        selected_month = datetime.strptime(selected_month, "%B").strftime("%m")
        projectoptions = [Projectnumber(project).legal for project in\
            self.__dbsession.query_distinct_projects(selected_year,
                                                     selected_month)]
        menu = self.__projectoptionmenu["menu"]
        menu.delete(0, "end")
        for project in projectoptions:
            menu.add_command(label=project, command=lambda value=project:\
                    self.__projectoptionmenu.setvar(\
                        self.__projectoptionmenu.cget("textvariable"), value))
        if projectoptions:
            self.__projectoptionmenu.setvar(\
                self.__projectoptionmenu.cget("textvariable"),
                projectoptions[0])
        self._update_log()

    def _update_log(self, *args) -> None:
        self.__listbox.clear_selection()
        selected_year = self.__yearoption_var.get()
        selected_month = self.__monthoption_var.get()
        selected_month = datetime.strptime(selected_month, "%B").strftime("%m")
        selected_project = str(Projectnumber(self.__projectoption_var.get()))
        month_of_year: str = f"{selected_year}-{selected_month}"
        log: sqlite3.Cursor =\
            self.__dbsession.query_log(selected_project, month_of_year)
        logbook = LogBook(log)
        self.__listbox.update_list(logbook.records)
        self._lookup_callback(logbook.records)

    def _lookup_callback(self, selection:List[LogRecord]) -> None:
        total = sum(record.value for record in selection)
        self.__totalvalue_var.set(\
            locale.format_string("%+.2f", total, grouping=True))