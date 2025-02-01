import locale
locale.setlocale(locale.LC_ALL, "")

from typing import Self

from record.record import Record
import utils.textrep as textrep


TRANSLATE_ATTRIBUTES = {
    "cikkszam": "articlenumber",
    "keszlet": "stock",
    "megnevezes": "name",
    "becenev": "nickname",
    "gyarto": "manufacturer",
    "leiras": "description",
    "megjegyzes": "comment",
    "egyseg": "unit",
    "egysegar": "unitprice",
    "kiszereles": "packaging",
    "hely": "place",
    "lejarat": "shelflife",
    "gyartasido": "productiondate",
    "szin": "color",
    "jeloles": "notation",
    "letrehozas": "created",
    "utolso_modositas": "modified"
}


class StockItemRecord(Record):
    """Handles a single item in the stock."""

    def __init__(self, **kwargs) -> None:
        """Setting the articlenumber attribute explicitly is important:
        If data is coming from a database source, it's the primary key.
        If data is gathered from a gui, it's a new item, it doesn't have any
        primary key yet."""
        self.articlenumber = None
        super().__init__(translate_attributes=TRANSLATE_ATTRIBUTES, **kwargs)

    def __str__(self) -> str:
        space = " " if self.manufacturer else ""
        return "{:<41} {:>10} {:<7}".format(
                (self.manufacturer + space + self.name)[0:41],
                locale.format_string(f="%.2f", val=self.stock, grouping=True),
                self.unit)

    def __bool__(self) -> bool:
        try:
            bool(self.name) and\
            bool(self.unit)
            stock = float(self.stock)
            unitprice = float(self.unitprice)
            return (stock >= 0) and (unitprice >= 0)
        except (AttributeError, ValueError):
            return False

    def __float__(self) -> float:
        return float(self.stock) * float(self.unitprice) if bool(self) else 0.0

    def contains(self, term:str) -> bool:
        for attribute in TRANSLATE_ATTRIBUTES.values():
            if term.lower() in str(getattr(self, attribute, None)).lower():
                return True
        return False

    def apply_change(self) -> None:
        """Change is signed: - for withdraw, + for deposit"""
        assert  hasattr(self, "change")
        self.stock += self.change

    def undo_change(self) -> None:
        """Change is signed: - for withdraw, + for deposit"""
        assert  hasattr(self, "change")
        self.stock -= self.change

    def is_almost_same(self, item:Self) -> bool:
        if textrep.asci(item.name) in textrep.asci(self.name) and\
            self.unitprice == item.unitprice:
            return True
        else:
            return False

    @property
    def withdraw_view(self) -> str:
        assert hasattr(self, "change")
        space = " " if self.manufacturer else ""
        return "{:<41} {:>10} {:<7}".format(
                (self.manufacturer + space + self.name)[0:41],
                locale.format_string(f="%+.2f", val=self.change, grouping=True),
                self.unit)

    @property
    def tooltip_view(self) -> str:
        return f"kiszerelés: {self.packaging} {self.unit}"