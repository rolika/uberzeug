from datetime import date
from typing import Iterable

from scripts.databasesession import DatabaseSession
from scripts.szam_megjelenites import *


class Rep:
    """A reprezentációs osztály a terminálon kijelzésekhez és a fileexportokhoz
    biztosít vonalat, címsort, fejlécet."""

    def line(char:str="_", length:int=80) -> str:
        return "".join(char for _ in range(length))


    def headline(text:str) -> str:
        head = " ".join(char.upper() for char in text)
        return "{}{:^80}{}{}".format(Rep.line(), head, "\n", Rep.line())


    def header(fillchar:str="", **kwargs:dict[str,int]) -> str:
        fmtspec = ("{:" + fillchar + "<" + str(kwargs[word]) + "}" \
                    for word in kwargs)
        header = "".join(fmtspec)\
            .format(*(word.capitalize() for word in kwargs.keys()))
        return f"{header}\n{Rep.line()}"

    def stock2str(session:DatabaseSession, articles:Iterable[int]) -> str:
        """Build a string of the presented articles to show the stock."""
        result = ""
        for i, article in enumerate(articles):
            record = session.select_item(article).fetchone()
            if record["keszlet"]:
                result += "{:>6}  {:<28} {:>8} {:<3} {:>9} Ft/{:<4}{:>10} Ft\n"\
                        .format(format(i + 1, "0=5"),
                            record["megnevezes"][0:28],
                            ezresv(format(float(record["keszlet"]), ".0f")),
                            record["egyseg"][:3],
                            ezresv(record["egysegar"]),
                            record["egyseg"][:3],
                            ezresv(int(float(record["keszlet"])\
                                       * float(record["egysegar"]))))
        return result

    def waybill2str(articles:dict) -> str:
        """Build a string of the presented articles to show the waybill."""
        result = ""
        for i, article in enumerate(articles):
            result += "{:>6}   {:<50} {:>12} {}\n"\
                        .format(format(i + 1, "0=5"),
                                       article["megnevezes"][0:49],
                                       ezresv(format(abs(article["valtozas"]),\
                                                     ".2f")),
                                       article["egyseg"])
        return result

    def waybill_header(organization:tuple, costcentre:tuple) -> str:
        result = ("\nSzállító:                                Projekt/Vevő:")
        for row in zip(organization, costcentre):
            result += "\n{:<41}{}".format(row[0], row[1])
        result += "\n\n"
        return result

    def waybill_footer() -> str:
        d = date.today()
        result = "\nKelt: Herend, {}\n\n\n\n\n".format(d.strftime("%Y.%m.%d."))
        result += "\n\n\n\n"
        result +=\
            "              ___________________          ___________________\n"
        result += "                     kiadta                     átvette\n"
        result += "                 Hartmann Zoltán\n"
        return result

    def show_stock(session:DatabaseSession,
                   articles:Iterable[int],
                   value:float) -> str:
        d = date.today()
        result = ""
        result += Rep.headline("raktárkészlet")
        result += Rep.header(sorszám=8,
                             megnevezés=33,
                             készlet=14,
                             egységár=16,
                             érték=9)
        result += Rep.stock2str(session, articles)
        result += Rep.line()
        result += "Kiválasztás értéke összesen:                            \
         {:>12} Ft\n".format(ezresv(value))
        result += Rep.line()
        result += "{}-i állapot.\n".format(d.strftime("%Y.%m.%d"))
        return result

    def show_waybill(waybill:list,
                     organization:tuple[str],
                     customer:tuple[str]) -> str:
        result = Rep.headline("szállítólevél")
        result += Rep.waybill_header(organization, customer)
        result += Rep.header(sorszám=9, megnevezés=54, mennyiség=10, egység=7)
        result += Rep.waybill2str(waybill)
        result += Rep.line()
        result += Rep.waybill_footer()
        return result
    
    def waybillpanel_header() -> str:
        return "ssz. {:<41} {:>10} {:<7}mégse".format("megnevezés", "változás", "egység")