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
        self._value = self.unitprice * self.change

    def __str__(self) -> str:
        return "{:<41} {:>10} {:<7}".format(
            self.name[0:41],
            locale.format_string(f="%+.2f", val=self.change, grouping=True),
            self.unit)

    def is_referring_to(self, stockitem:StockItemRecord) -> bool:
        """Returns True if the name of the stocitem is referring to the name
        of the log record."""
        return asci(stockitem.name) in asci(self.name)

    def contains(self, term:str) -> bool:
        for attribute in TRANSLATE_ATTRIBUTES.values():
            if asci(term) in\
                asci(str(getattr(self, attribute, None))):
                return True
        return False

    @property
    def listview(self) -> str:
        return "{name:<28} {change:>6} {unit:<4} x {up:>7} = {value:>13} Ft".\
                format(name=self.name,
                       change=locale.format_string(f="%+.2f", val=self.change,
                                                   grouping=True),
                       unit=self.unit,
                       up=locale.format_string(f="%+.2f", val=self.unitprice,
                                               grouping=True),
                       value=locale.format_string(f="%+.2f", val=self._value,
                                                  grouping=True))