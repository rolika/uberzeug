import locale
locale.setlocale(locale.LC_ALL, "")

from scripts.projectnumber import Projectnumber
from scripts.record import Record
from scripts.stockitemrecord import StockItemRecord


TRANSLATE_ATTRIBUTES = {
    "azonosito": "primary_key",
    "megnevezes": "name",
    "egysegar": "unitprice",
    "egyseg": "unit",
    "valtozas": "change",
    "datum": "date",
    "projektszam": "projectnumber"
}


class LogRecord(Record):
    """Handles a single record in the logbook."""
    def __init__(self, **kwargs) -> None:
        super().__init__(translate_attributes=TRANSLATE_ATTRIBUTES, **kwargs)
    
    @classmethod
    def from_withdraw(cls, item:StockItemRecord) -> object:
        kwargs = {
            "name": f"{item.manufacturer} {item.name}",
            "unitprice": item.unitprice,
            "unit": item.unit,
            "change": item.change,
            "projectnumber": item.projectnumber
        }
        delattr(item, "change")
        delattr(item, "projectnumber")
        return cls(**kwargs)

    def __str__(self) -> str:
        return "{:<41} {:>10} {:<7}".format(
                (self.name)[0:41],
                locale.format_string(f="%+.2f", val=self.change, grouping=True),
                self.unit)