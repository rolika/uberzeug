from datetime import datetime, date, timedelta
import locale
locale.setlocale(locale.LC_ALL, "")
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from utils.constants import *
from persistence.databasesession import DatabaseSession
from utils.projectnumber import Projectnumber
from record.logbook import LogBook
from record.logrecord import LogRecord


class TransferDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, title:str, project:Projectnumber,
                 logrecord:LogRecord, dbsession:DatabaseSession) -> None:
        title = f"{project.legal}: {title}"
        self.__project = project
        self.__logrecord = logrecord
        self.__dbsession = dbsession
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        box = Frame(self)
        label = Label(box, text=self.__logrecord.listview)
        label.pack(padx=PADX, pady=PADY)
        self.__projectoption_var: StringVar = StringVar()
        self.__projectcombobox: ttk.Combobox = ttk.Combobox(
            box, textvariable=self.__projectoption_var, state="readonly")
        self.__projectoption_var.trace("w", self._transfer_log)
        projectoptions = [project.legal for project in\
                self.__dbsession.query_all_distinct_projects()]
        self.__projectcombobox["values"] = projectoptions
        self.__projectoption_var.set(self.__project.legal)
        self.__projectcombobox.pack(side=LEFT, fill=X, expand=True)
        box.pack()
        return None

    def _transfer_log(self, *args) -> None:
        selected_project = self.__projectoption_var.get()
        if selected_project == self.__project.legal:
            return
        if not messagebox.askokcancel("Átvezetés megerősítése",
                                    f"Átvezeted {selected_project} projektbe?"):
            self.__projectoption_var.set(self.__project.legal)
            return
        self.__dbsession.transfer_log(self.__logrecord.articlenumber,
                                      Projectnumber(selected_project))
        self.destroy()