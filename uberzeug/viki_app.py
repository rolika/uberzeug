import locale
locale.setlocale(locale.LC_ALL, "")

import databasesession as dbs, logbook as lb, climenu as clm
from datetime import date
from rep import Rep


class App():
    def __init__(self, db="data/adatok.db") -> None:
        self._dbs = dbs.DatabaseSession(db)

    def run(self) -> None:
        print(Rep.headline("utókalkulátor"))
        while True:
            month = self._choose_month()
            logbook = self._choose_project(month)
            print(Rep.line())
            print(Rep.header(megnevezés=30, változás=12, egységár=19, érték=1))
            for record in logbook.records:
                print(record)
            print(Rep.line())
            print("{:>51} {:>14} Ft".format("Összesen:", logbook.total))
            print(Rep.line())

    def _choose_month(self) -> str:
        months_as_text = [date.fromisoformat(month[0]+"-01").strftime("%Y. %B")\
                          for month in self._dbs.query_months()]
        months_iso = [month[0] for month in self._dbs.query_months()]
        month_menu = clm.CliMenu(months_as_text, title="Válassz hónapot!")
        month_menu.show()
        choice = month_menu.listen()
        return months_iso[choice]

    def _choose_project(self, month:str) -> str:
        logbooks = [lb.LogBook(self._dbs.query_log(project[0], month))\
                    for project in self._dbs.query_projects(month)]
        project_menu = clm.CliMenu(logbooks, title="Válassz projektet!")
        project_menu.show()
        choice = project_menu.listen()
        return logbooks[choice]


if __name__ == "__main__":
    app = App()
    app.run()
