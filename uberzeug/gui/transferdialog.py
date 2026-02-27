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
                 logrecord:LogRecord, dbsession:DatabaseSession,
                 yearmonth:date) -> None:
        title = f"{project.legal}: {title}"
        self.__project = project
        self.__logrecord = logrecord
        self.__dbsession = dbsession
        self.__yearmonth = yearmonth.strftime("%Y-%m")
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        box = Frame(self)
        label = Label(box, text=self.__logrecord.listview)
        label.pack(padx=PADX, pady=PADY)
        box.pack()
        return None