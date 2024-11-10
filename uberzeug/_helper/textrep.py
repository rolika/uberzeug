"""Various function for text representation."""


from datetime import date


def line(char:str="_", length:int=80) -> str:
    return "".join(char for _ in range(length))


def headline(text:str) -> str:
    head = " ".join(char.upper() for char in text)
    return "{}{:^80}{}{}".format(line(), head, "\n", line())


def header(fillchar:str="", **kwargs:dict[str,int]) -> str:
    fmtspec = ("{:" + fillchar + "<" + str(kwargs[word]) + "}" \
                for word in kwargs)
    header = "".join(fmtspec)\
        .format(*(word.capitalize() for word in kwargs.keys()))
    return f"{header}\n{line()}"

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
    result = headline("szállítólevél")
    result += waybill_header(organization, customer)
    result += header(sorszám=9, megnevezés=54, mennyiség=10, egység=7)
    result += line()
    result += waybill_footer()
    return result


def waybillpanel_header() -> str:
    return "ssz. {:<41} {:>10} {:<7}mégse".format("megnevezés", "változás", "egység")