from datetime import date
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
        Label(box, text=self.__logrecord.name)\
            .pack(padx=PADX, pady=PADY)
        Label(box,
              text=f"{locale.format_string(f='%+.2f',
                    val=self.__logrecord.change,
                    grouping=True)} {self.__logrecord.unit} x ")\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        self.__unitprice_var = StringVar()
        entry =Entry(box, justify=RIGHT, textvariable=self.__unitprice_var,
                     width=9)
        entry.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__unitprice_var.set(locale.format_string(f="%.2f",
            val=self.__logrecord.unitprice, grouping=True))
        entry.select_range(0, END)
        self.__unitprice_var.trace("w", self._update_values)
        Label(box, text=f"Ft/{self.__logrecord.unit} = ")\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        self.__value_var = StringVar()
        Label(box, textvariable=self.__value_var)\
            .pack(padx=PADX, pady=PADY)
        self.__value_var.set(locale.format_string(f="%+.2f",
            val=self.__logrecord.value, grouping=True) + " Ft")
        box.pack(padx=PADX, pady=PADY)
        box = Frame(self)
        Label(box, text="Átvezetés célprojektje:")\
            .pack(side=LEFT, padx=PADX, pady=PADY)
        self.__projectoption_var: StringVar = StringVar()
        self.__projectcombobox: ttk.Combobox = ttk.Combobox(
            box, textvariable=self.__projectoption_var, state="readonly")
        projectoptions = [project.legal for project in\
                self.__dbsession.query_distinct_projects(self.__yearmonth)]
        self.__projectcombobox["values"] = projectoptions
        self.__projectoption_var.set(self.__project.legal)
        self.__projectoption_var.trace("w", self._update_values)
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
        self._update_values()
        return entry

    def apply(self):
        selected_project = self.__projectoption_var.get()
        if selected_project == self.__project.legal and\
            self._get_unitprice() == self.__logrecord.unitprice:
            return
        if not messagebox.askokcancel("Átvezetés megerősítése",
                                    f"Átvezeted {selected_project} projektbe?",
                                    parent=self):
            self.__projectoption_var.set(self.__project.legal)
            return
        if selected_project != self.__project.legal:
            self.__dbsession.transfer_log(self.__logrecord.articlenumber,
                                          Projectnumber(selected_project))
        if self._get_unitprice() != self.__logrecord.unitprice:
            self.__dbsession.update_log_unitprice(\
                self.__logrecord.articlenumber, self._get_unitprice())
        self.destroy()

    def _update_values(self, *args):
        project = Projectnumber(self.__projectoption_var.get())
        unitprice = self._get_unitprice()
        self.__value_var.set(locale.format_string(f="%+.2f",
            val=unitprice * self.__logrecord.change, grouping=True) + " Ft")
        if project == self.__project:
            self.__selected_project_var.set("")
            difference = self.__logrecord.change *\
                (self.__logrecord.unitprice - unitprice)
            project_turnover =\
                self._get_logbook_value(self.__project, -difference)
            selected_project_turnover = ""
        else:
            self.__selected_project_var.set(\
                f"{project.legal} anyagköltsége átvezetés után:")
            difference = self.__logrecord.change * unitprice
            selected_project_turnover = self._get_logbook_value(project,
                                                                difference)
            if unitprice != self.__logrecord.unitprice:
                difference = self.__logrecord.change *\
                    self.__logrecord.unitprice
            project_turnover = self._get_logbook_value(self.__project,
                                                       -difference)
        self.__project_turnover_value.set(project_turnover)
        self.__selected_project_turnover_value.set(selected_project_turnover)

    def _get_logbook_value(self, project:Projectnumber,
                           difference:float) -> str:
        logbook = LogBook(\
            self.__dbsession.query_log(project, self.__yearmonth))
        return locale.format_string("%+.2f", logbook.total + difference,
                                    grouping=True) + " Ft"

    def _get_unitprice(self) -> float:
        unitprice = self.__unitprice_var.get().replace(" ", "")
        try:
            return locale.atof(unitprice)
        except ValueError:
            return self.__logrecord.unitprice
