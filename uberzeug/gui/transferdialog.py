from datetime import date
import locale
locale.setlocale(locale.LC_ALL, "")
import locale
locale.setlocale(locale.LC_ALL, "")
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog

from utils.constants import *
from persistence.databasesession import DatabaseSession
from utils.projectnumber import Projectnumber
from record.logbook import LogBook
from record.logrecord import LogRecord


class TransferDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, title:str, project:Projectnumber,
                 yearmonth:date, logrecord:LogRecord,
                 dbsession:DatabaseSession) -> None:
        title = f"{project.legal}: {title}"
        self.__project = project
        self.__yearmonth = yearmonth
        self.__logrecord = logrecord
        self.__dbsession = dbsession
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        box = Frame(self)
        Label(box, text=self.__logrecord.listview).pack(padx=PADX, pady=PADY)
        self.__projectoption_var: StringVar = StringVar()
        self.__projectcombobox: ttk.Combobox = ttk.Combobox(
            box, textvariable=self.__projectoption_var, state="readonly")
        projectoptions = [project.legal for project in\
                self.__dbsession.query_all_distinct_projects()]
        self.__projectcombobox["values"] = projectoptions
        self.__projectoption_var.set(self.__project.legal)
        self.__projectoption_var.trace("w", self._update_project_selection)
        self.__projectcombobox.pack(fill=X, expand=True)
        Label(box,
              text=f"{self.__project.legal} anyagköltsége átkönyvelés után:")\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        self.__turnover_value = StringVar()
        Label(box, textvariable=self.__turnover_value)\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        box.pack()
        self._update_project_selection()
        return None

    def apply(self):
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

    def _update_project_selection(self, *args):
        project_logbook = LogBook(\
            self.__dbsession.query_log_by_month_and_project(self.__yearmonth,
                                                            self.__project))
        self.__turnover_value.set(\
            locale.format_string("%+.2f",
                                 project_logbook.total, grouping=True) + " Ft")