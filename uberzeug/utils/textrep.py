"""Various function for text representation."""


import locale
locale.setlocale(locale.LC_ALL, "")
from datetime import date
import re
from typing import List

import utils.constants as ct
from utils.constants import *
from utils.projectnumber import Projectnumber


def line(char:str="_", length:int=80) -> str:
    return "".join(char for _ in range(length))


def explode(text:str, filler:str=" ", width:int=1) -> str:
    filler = filler * width
    return filler.join(char for char in text)


def headline(text:str, explode_it:bool=True, uppercase:bool=True) -> str:
    if explode_it:
        text = explode(text)
    if uppercase:
        text = text.upper()
    return f"{text:^80}"


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
    result += f"Kelt: Herend, {d.strftime('%Y.%m.%d.')}\n\n\n\n\n"
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


def turnover_header(projectnumber:Projectnumber, yearmonth:str,
                    lookup_term:str) -> str:
    result = line() + "\n"
    year = yearmonth.split(".")[0]
    month = yearmonth.split(".")[1].strip()
    if month == ct.SHOW_ALL:
        month = "év"
    result += headline(f"{projectnumber.legal} - {year}. {month}i forgalom",
                       explode_it=False, uppercase=False) + "\n"
    result += line() + "\n"
    if lookup_term:
        result += f"Keresési kifejezés: {lookup_term.capitalize()}\n"
        result += line() + "\n"
    return result


def turnover_footer(total:float) -> str:
    result = line() + "\n"
    result +=\
    f"Összesen: {locale.format_string('%+.2f', total, grouping=True):>66} Ft\n"
    result += line() + "\n"
    d = date.today()
    result += f"Kelt: Herend, {d.strftime('%Y. %B %d.')}\n"
    return result


def asci(text:str) -> str:
    """Return the input as lower-cased alphanumeric text to avoid confusion."""
    return "".join(re.findall("[a-z0-9]", str(text).lower().\
        translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))))


if __name__ == "__main__":
    print(line())
    print(headline("this is a headline"))
    print(line())
    print(asci("árvíz22tűrő_-22tükörfúrógép"))