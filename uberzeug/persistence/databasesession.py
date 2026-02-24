from datetime import date
import pathlib
import sqlite3
from typing import List

from utils.constants import *
from utils.projectnumber import Projectnumber
from record.logrecord import LogRecord
from record.stockitemrecord import StockItemRecord


class DatabaseSession(sqlite3.Connection):
    """This class handles all database-related stuff."""

    def __init__(self, filepath:str) -> None:
        """Initialize an sqlite database connection."""
        super().__init__(pathlib.Path(filepath))
        self.row_factory = sqlite3.Row  # access results with column-names
        self._create_tables()

    def _create_tables(self):
        with self:
            self.execute("""
                CREATE TABLE IF NOT EXISTS raktar(
                    cikkszam INTEGER PRIMARY KEY ASC,
                    keszlet,
                    megnevezes,
                    becenev,
                    gyarto,
                    leiras,
                    megjegyzes,
                    egyseg,
                    egysegar,
                    kiszereles,
                    hely,
                    lejarat,
                    gyartasido,
                    szin,
                    jeloles,
                    letrehozas,
                    utolso_modositas);
                """)
            self.execute("""
                CREATE TABLE IF NOT EXISTS raktar_naplo(
                    azonosito INTEGER PRIMARY KEY ASC,
                    megnevezes,
                    egysegar,
                    egyseg,
                    valtozas,
                    datum,
                    projektszam);
                """)

    def _select_all_items(self) -> sqlite3.Cursor:
        return self.execute("""
            SELECT  cikkszam,
                    CAST(keszlet AS REAL) AS keszlet,
                    megnevezes,
                    becenev,
                    gyarto,
                    leiras,
                    megjegyzes,
                    egyseg,
                    CAST(egysegar AS INT) AS egysegar,
                    kiszereles,
                    hely,
                    lejarat,
                    gyartasido,
                    szin,
                    jeloles,
                    letrehozas,
                    utolso_modositas
            FROM raktar ORDER BY gyarto, megnevezes;
               """)

    def query_log(self, projectnumber:Projectnumber,
                  date_:date) -> sqlite3.Cursor:
        """Query items belonging to projectnumber and inserted in month.
        Both arguments should be verified for proper formatting before calling:
        projectnumber:  yy_nnn
        month:          yyyy-mm"""
        month = date_.strftime("%Y-%m")
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE projektszam = ?
            AND strftime('%Y-%m', datum) = ?
            GROUP BY megnevezes, egysegar;
        """, (str(projectnumber), month))

    def query_log_by_year(self, date_:date) -> sqlite3.Cursor:
        year = date_.strftime("%Y")
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE strftime('%Y', datum) = ?
            GROUP BY megnevezes, egysegar;
        """, (year, ))

    def query_log_by_month(self, date_:date) -> sqlite3.Cursor:
        # hasn't much sense, but it's easier than exclude the option
        month = date_.strftime("%m")
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE strftime('%m', datum) = ?
            GROUP BY megnevezes, egysegar;
        """, (month, ))

    def query_log_by_project(self,
                             projectnumber:Projectnumber) -> sqlite3.Cursor:
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE projektszam = ?
            GROUP BY megnevezes, egysegar;
        """, (str(projectnumber), ))

    def query_log_by_year_and_month(self, date_:date) -> sqlite3.Cursor:
        yearmonth = date_.strftime("%Y-%m")
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE strftime('%Y-%m', datum) = ?
            GROUP BY megnevezes, egysegar;
        """, (yearmonth, ))

    def query_log_by_year_and_project(self, date_:date,
                                projectnumber:Projectnumber) -> sqlite3.Cursor:
        year = date_.strftime("%Y")
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE strftime('%Y', datum) = ?
            AND projektszam = ?
            GROUP BY megnevezes, egysegar;
        """, (year, str(projectnumber), ))

    def query_log_by_month_and_project(self, date_:date,
                                projectnumber:Projectnumber) -> sqlite3.Cursor:
        # hasn't much sense either
        month = date_.strftime("%m")
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE strftime('%m', datum) = ?
            AND projektszam = ?
            GROUP BY megnevezes, egysegar;
        """, (month, str(projectnumber), ))

    def query_log_by_all(self) -> sqlite3.Cursor:
        return self.execute(f"""
            SELECT {LOG_COLUMNS}, SUM(valtozas) AS total_change
            FROM raktar_naplo
            GROUP BY megnevezes, egysegar;
        """)

    def query_distinct_years(self) ->List[str]:
        """Query distinct years in descending order."""
        years = self.execute("""
            SELECT DISTINCT strftime('%Y', datum) AS year
            FROM raktar_naplo
            ORDER BY year DESC;
        """)
        return [year["year"] for year in years]

    def query_distinct_months(self, year:str) -> List[str]:
        """Query distinct months in descending order."""
        months = self.execute("""
            SELECT DISTINCT strftime('%m', datum) AS month
            FROM raktar_naplo
            WHERE strftime('%Y', datum) = ?
            ORDER BY month DESC;
        """, (year, ))
        return [date(1900, int(month["month"]), 1).strftime("%B")\
                for month in months]

    def query_all_distinct_months(self) -> List[str]:
        """Query distinct months in descending order."""
        months = self.execute("""
            SELECT DISTINCT strftime('%m', datum) AS month
            FROM raktar_naplo
            ORDER BY month DESC;
        """)
        return [date(1900, int(month["month"]), 1).strftime("%B")\
                for month in months]

    def query_distinct_projects(self, date_:date) -> List[Projectnumber]:
        yearmonth = date_.strftime("%Y-%m")
        projects = self.execute("""
            SELECT DISTINCT projektszam AS projectnumber
            FROM raktar_naplo
            WHERE strftime('%Y-%m', datum) = ?
            ORDER BY projektszam ASC;
        """, (yearmonth, ))
        return [Projectnumber(project["projectnumber"]) for project in projects]

    def query_distinct_projects_by_month(self,
                                         date_:date) -> List[Projectnumber]:
        month = date_.strftime("%m")
        projects = self.execute("""
            SELECT DISTINCT projektszam AS projectnumber
            FROM raktar_naplo
            WHERE strftime('%m', datum) = ?
            ORDER BY projektszam ASC;
        """, (month, ))
        return [Projectnumber(project["projectnumber"]) for project in projects]

    def query_distinct_projects_by_year(self,
                                         date_:date) -> List[Projectnumber]:
        year = date_.strftime("%Y")
        projects = self.execute("""
            SELECT DISTINCT projektszam AS projectnumber
            FROM raktar_naplo
            WHERE strftime('%Y', datum) = ?
            ORDER BY projektszam ASC;
        """, (year, ))
        return [Projectnumber(project["projectnumber"]) for project in projects]

    def query_all_distinct_projects(self) -> List[Projectnumber]:
        """Query distinct projectnumbers in ascending order."""
        projects = self.execute("""
            SELECT DISTINCT projektszam AS projectnumber
            FROM raktar_naplo
            ORDER BY projektszam ASC;
        """)
        return [Projectnumber(project["projectnumber"]) for project in projects],

    def load_all_items(self) -> List[StockItemRecord]:
        return [StockItemRecord(**item) for item in self._select_all_items()]

    def load_withdrawable_items(self) -> List[StockItemRecord]:
        return [StockItemRecord(**item) for item in self._select_all_items()
                if item["keszlet"] > 0]

    def log_stock_change(self, items:List[StockItemRecord],
                         projectnumber:Projectnumber) -> None:
        self.update_stock(items)
        with self:
            for item in items:
                space = " " if item.manufacturer else ""
                name = item.manufacturer + space + item.name
                self.execute("""
                    INSERT INTO raktar_naplo (megnevezes, egysegar, egyseg,
                                            valtozas, datum, projektszam)
                    VALUES (?, ?, ?, ?, date(), ?)
                """, (name, item.unitprice, item.unit, item.change,
                    str(projectnumber)))

    def _load_log_entries(self, projectnumber:Projectnumber) -> List[LogRecord]:
        logentries = self.execute("""
            SELECT *, SUM(valtozas) AS total_change
            FROM raktar_naplo
            WHERE projektszam = ?
            GROUP BY megnevezes;""", (str(projectnumber), ))
        return [LogRecord(**item) for item in logentries]

    def get_project_stock(self, projectnumber:Projectnumber)\
        -> List[StockItemRecord]:
        all_items = self.load_all_items()
        log_records = self._load_log_entries(projectnumber)
        project_stock = set()
        for entry in log_records:
            for item in all_items:
                change = abs(entry.change)
                if entry.is_referring_to(item) and change > 0:
                    setattr(item, "backup_stock", item.stock)
                    item.stock = change
                    project_stock.add(item)
                    break
        return sorted(project_stock, key=str)

    def lookup(self, newitem:StockItemRecord) -> StockItemRecord|None:
        for stockitem in self.load_all_items():
            if stockitem.is_almost_same(newitem):
                return stockitem
        return None

    def update(self, stockitem:StockItemRecord) -> None:
        with self:
            self.execute("""
        UPDATE raktar
        SET keszlet = ?, megnevezes = ?, becenev = ?, gyarto = ?, leiras = ?,
            szin = ?, megjegyzes = ?, egyseg = ?, egysegar = ?, kiszereles = ?,
            hely = ?, lejarat = ?, gyartasido = ?, utolso_modositas = date()
        WHERE cikkszam = ?;
        """, (stockitem.stock, stockitem.name, stockitem.nickname,
              stockitem.manufacturer, stockitem.description, stockitem.color, stockitem.comment, stockitem.unit, stockitem.unitprice,
              stockitem.packaging, stockitem.place, stockitem.shelflife, stockitem.productiondate, stockitem.articlenumber))

    def insert(self, stockitem:StockItemRecord) -> None:
        with self:
            self.execute("""
        INSERT INTO raktar (keszlet, megnevezes, becenev, gyarto, leiras, szin,
                            megjegyzes, egyseg, egysegar, kiszereles, hely,
                            lejarat, gyartasido, letrehozas, utolso_modositas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date(), date())
        """, (stockitem.stock, stockitem.name, stockitem.nickname,
              stockitem.manufacturer, stockitem.description, stockitem.color, stockitem.comment, stockitem.unit, stockitem.unitprice,
              stockitem.packaging, stockitem.place, stockitem.shelflife, stockitem.productiondate))

    def update_stock(self, items:List[StockItemRecord]) -> None:
        with self:
            for item in items:
                self.execute("""
                    UPDATE raktar
                    SET keszlet = ?, utolso_modositas = date()
                    WHERE cikkszam = ?;
                """, (item.stock, item.articlenumber))

    def delete(self, item:StockItemRecord) -> None:
        with self:
            self.execute("""
                        DELETE FROM raktar
                        WHERE cikkszam = ?;
                         """, (item.articlenumber, )),

    def select_all_items_for_export(self) -> List[StockItemRecord]:
        """Returns all items that are withdawable, i.e. with stock > 0 for
        export, in descendding order by value, i.e. stock * unitprice. """
        return sorted(self.load_withdrawable_items(),
                      key=lambda item: item.value, reverse=True)