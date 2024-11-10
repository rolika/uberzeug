from datetime import date
from typing import Iterable

from uberzeug._persistence.databasesession import DatabaseSession


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