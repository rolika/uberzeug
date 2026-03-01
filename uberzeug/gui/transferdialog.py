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
        Label(box, text="Átvezetés célprojektje:")\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        self.__projectoption_var: StringVar = StringVar()
        self.__projectcombobox: ttk.Combobox = ttk.Combobox(
            box, textvariable=self.__projectoption_var, state="readonly")
        projectoptions = [project.legal for project in\
                self.__dbsession.query_distinct_projects(self.__yearmonth)]
        self.__projectcombobox["values"] = projectoptions
        self.__projectoption_var.set(self.__project.legal)
        self.__projectoption_var.trace("w", self._update_project_selection)
        self.__projectcombobox.pack(fill=X, expand=True)
        box.pack(padx=PADX, pady=PADY)

        box = Frame(self)
        text = f"{self.__project.legal} anyagköltsége átvezetés után:"
        Label(box, text=text).pack(side=LEFT, padx=PADX, pady=PADY)
        self.__project_turnover_value = StringVar()
        Label(box, textvariable=self.__project_turnover_value)\
            .pack(padx=PADX, pady=PADY)
        box.pack(padx=PADX, pady=PADY)

        box = Frame(self)
        self.__selected_project_var = StringVar()
        Label(box, textvariable=self.__selected_project_var)\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        self.__selected_project_turnover_value = StringVar()
        Label(box, textvariable=self.__selected_project_turnover_value)\
            .pack(padx=PADX, pady=PADY)
        box.pack(padx=PADX, pady=PADY)
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
        project = Projectnumber(self.__projectoption_var.get())
        self.__selected_project_var.set(\
            f"{project.legal} anyagköltsége átvezetés után:")
        difference = 0.0 if project == self.__project\
            else self.__logrecord.value
        self.__project_turnover_value.set(\
            self._get_logbook_value(self.__project, -difference))
        self.__selected_project_turnover_value.set(\
            self._get_logbook_value(project, difference))

    def _get_logbook_value(self, project:Projectnumber,
                           difference:float) -> str:
        logbook = LogBook(\
            self.__dbsession.query_log_by_month_and_project(self.__yearmonth,
                                                            project))
        return locale.format_string("%+.2f", logbook.total + difference,
                                    grouping=True) + " Ft"