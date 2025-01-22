import difflib
import locale
locale.setlocale(locale.LC_ALL, "")

from uberzeug._record.record import Record
from uberzeug._record.stockitemrecord import StockItemRecord


TRANSLATE_ATTRIBUTES = {
    "azonosito": "articlenumber",
    "megnevezes": "name",
    "egyseg": "unit",
    "egysegar": "unitprice",
    "valtozas": "change",
    "datum": "date",
    "projektszam": "projectnumber",
    "total_change": "total_change"
}


class LogRecord(Record):
    """Handles a single record in the inventory log."""

    def __init__(self, translate_attributes=TRANSLATE_ATTRIBUTES,
                 **kwargs) -> None:
        super().__init__(translate_attributes, **kwargs)
        self.change = self.total_change

    def __str__(self) -> str:
        return "{:<41} {:>10} {:<7}".format(
            self.name[0:41],
            locale.format_string(f="%+.2f", val=self.change, grouping=True),
            self.unit)
    
    def is_referring_to(self, stockitem:StockItemRecord) -> bool:
        """Returns True if the name of the stocitem is contained in the name
        of the log record."""
        close = difflib.get_close_matches(stockitem.name, [self.name],
                                          cutoff=0.9)
        return len(close) > 0