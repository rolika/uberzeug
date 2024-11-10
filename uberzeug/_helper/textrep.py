"""Various function for text representation."""


from datetime import date
from typing import List

from uberzeug._helper.constants import *
from uberzeug._helper.projectnumber import Projectnumber


def line(char:str="_", length:int=80) -> str:
    return "".join(char for _ in range(length))


def explode(text:str, filler:str=" ", width:int=1) -> str:
    filler = filler * width
    return filler.join(char for char in text)


def headline(text:str) -> str:
    return f"{explode(text).upper():^80}"


def waybill_header(organization:List[str]=ORGANIZATION,
                   costcentre:List[str]=CLIENT,
                   projectnumber:Projectnumber= None) -> str:
    if projectnumber:
        costcentre[0] = projectnumber.legal
    result = line() + "\n"
    result += headline(WAYBILL_TITLE) + "\n"
    result += line() + "\n"
    result += ("Szállító:                                Projekt/Vevő:\n")
    for row in zip(organization, costcentre):
        result += "{:<41}{}\n".format(row[0], row[1])
    result += line() + "\n"
    return result


def waybill_footer() -> str:
    d = date.today()
    result = line() + "\n\n"
    result += f"Kelt: Herend, {d.strftime("%Y.%m.%d.")}\n\n\n\n\n"
    result += "\n\n\n\n"
    result +=\
        "              ___________________          ___________________\n"
    result += "                     kiadta                     átvette\n"
    result += "               Hartmann Zoltán [ ]\n"
    result += "                Badics Zoltán [ ]\n"
    return result


def waybillpanel_header() -> str:
    return "ssz. {:<41} {:>10} {:<7}mégse"\
        .format("megnevezés", "változás", "egység")


if __name__ == "__main__":
    print(line())
    print(headline("this is a headline"))
    print(line())