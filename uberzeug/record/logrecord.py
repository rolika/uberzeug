import locale
locale.setlocale(locale.LC_ALL, "")

from utils.textrep import asci
from record.record import Record
from record.stockitemrecord import StockItemRecord


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
        """Returns True if the name of the stocitem is referring to the name
        of the log record."""
        return asci(stockitem.name) in asci(self.name)
    
    @property
    def controlling_view(self) -> str:
        return "{:<41} {:>10} {:<7} x {:<10} Ft/{:<7}".format(
            self.name[0:41],
            locale.format_string(f="%+.2f", val=self.change, grouping=True),
            self.unit, self.unitprice, self.unit)