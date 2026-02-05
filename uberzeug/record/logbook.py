from collections import namedtuple
from functools import reduce
from operator import attrgetter
from sqlite3 import Cursor

import record.logrecord as lr


LOG_COLUMNS = "megnevezes, egysegar, egyseg, valtozas, datum, projektszam"


class LogBook():
    """The logbook represents an ordered list of log records."""
    def __init__(self, query:Cursor) -> None:
        self._records = [lr.LogRecord(**item) for item in query]
        self._records.sort(key=attrgetter("value", "change"))

    def __str__(self) -> str:
        projectnumber = self._records[0].projectnumber
        return f"{projectnumber.legal}: {self.total:>15} Ft"

    @property
    def records(self) -> list[lr.LogRecord]:
        return self._records

    @property
    def total(self) -> int:
        return reduce(lambda x, y: x + y,
                      (record.value for record in self._records))