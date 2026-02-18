from functools import reduce
from operator import attrgetter
from sqlite3 import Cursor

import record.logrecord as lr


class LogBook():
    """The logbook represents an ordered list of log records."""
    def __init__(self, query:Cursor) -> None:
        self.__records = [lr.LogRecord(**item) for item in query]
        self.__records.sort(key=attrgetter("value", "change"))
        self._merge_same__records()

    @classmethod
    def from__records(cls, records:list[lr.LogRecord]) -> "LogBook":
        logbook = cls.__new__(cls)
        logbook.__records = records
        return logbook

    def __str__(self) -> str:
        projectnumber = self.__records[0].projectnumber
        return f"{projectnumber.legal}: {self.total:>15} Ft"

    @property
    def records(self) -> list[lr.LogRecord]:
        return self.__records

    @property
    def total(self) -> int:
        return reduce(lambda x, y: x + y,
                      (record.value for record in self.__records))

    def _merge_same__records(self) -> None:
        """Merge records with the same name and unitprice,
        and sum their values."""
        merged_records: list[lr.LogRecord] = []
        for record in self.__records:
            for merged in merged_records:
                if (record.name == merged.name)\
                    and (record.unitprice == merged.unitprice):
                    merged.change += record.change
                    merged.value += record.value
                    break
            else:
                merged_records.append(record)
        self.__records = merged_records