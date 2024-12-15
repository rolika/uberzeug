import enum

APPLICATION_TITLE = "ÜBERZEUG"
ORGANIZATION = ["Pohlen-Dach Hungária Bt.", "8440-Herend", "Dózsa utca 49."]
CLIENT = ["...................", "...................", "..................."]

LOG_COLUMNS = "megnevezes, egysegar, egyseg, valtozas, datum, projektszam"
DATABASE = r"data/adatok.db"

TITLE_IMAGE = r"data/titleimg.gif"
WINDOWS_ICON = r"data/pohlen.ico"
LINUX_ICON = r"data/pohlen.gif"

WAYBILLFOLDER = r"data/Szállítólevelek/"
EXTENSION = "txt"
STOCKNAME = "Raktárkészlet"
WITHDRAW_TITLE = "Kivét raktárból"
DEPOSIT_TITLE = "Bevételezés raktárba"
WAYBILL_TITLE = "Szállítólevél"
TAKEBACK_TITLE = "Visszavét projektről"
MODIFIY_TITLE = "Anyag módosítása"
DELETE_TITLE = "Anyag törlése"

PADX = 2
PADY = 2

PROJECTNUMBER_PATTERN = r"(?P<year>\d{2})[/ _-](?P<serial>\d{1,3})"
MIN_YEAR = 0
MAX_YEAR = 99
MIN_SERIAL = 0
MAX_SERIAL = 999

LOGFILE = r"data/uberzeug.log"

Mode = enum.Enum("Mode", [("WITHDRAW", 1),
                          ("TAKEBACK", 2),
                          ("DEPOSIT",  3),
                          ("DELETE", 4)])