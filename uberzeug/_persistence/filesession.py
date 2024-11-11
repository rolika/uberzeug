from datetime import date
import logging
import os
import pathlib
import socket
from typing import List

from uberzeug._helper import textrep
from uberzeug._helper.constants import *
from uberzeug._helper.projectnumber import Projectnumber
from uberzeug._record.stockitemrecord import StockItemRecord


class FileSession:
    """Class for handling file operations.
    This inventory uses file handling in one way as writing only.
    One can export the stock or its selected items, and a waybill will be
    exported whenever the stock is changed.
    The waybill exports come to project folder divided into years and months,
    like: 24_001 -> 2024 -> June.
    The waybill has a number which looks like 24_001_12, the latter being a
    serial number, which is always +1 of all waybills in the projectfolder."""
    def __init__(self, organization:List[str],
                 waybillfolder:str=WAYBILLFOLDER,
                 extension:str=EXTENSION) -> None:
        self.__waybillfolder = pathlib.Path(waybillfolder)
        self.__extension = extension
        self.__organization = organization
        self._create_waybillfolder()
        logging.basicConfig(filename=LOGFILE, encoding='utf-8',
                            format="%(levelname)s: %(asctime)s %(message)s",
                            datefmt="%Y.%m.%d %H:%M:%S", level=logging.INFO)

    def _create_waybillfolder(self) -> None:
        try:
            os.mkdir(self.__waybillfolder)
        except FileExistsError:
            pass

    def export(self, content:str) -> None:
        if self._projectnumber:
            waybill_number = "{}_{}".format(self._projectnumber,
                                            self._count_waybills() + 1,)
            filename = "{}.{}".format(waybill_number, self._extension)
        else:
            d = date.today()
            filename = "{}_{}.{}".format(self._stockname,
                                         d.strftime("%Y%m%d"),
                                         self._extension)
        with open(self._exportfolder / filename, "w") as f:
            if self._projectnumber:
                f.write("{:>79}".format("Szállítólevél száma: {}\n"\
                                        .format(waybill_number)))
            f.write(content)

    def export_waybill(self, items:List[StockItemRecord],
                       projectnumber:Projectnumber) -> None:
        exportfolder = self._get_exportfolder(projectnumber)
        projectfolder = pathlib.Path("/".join(exportfolder.parts[:-2]))
        next_waybill_number = self._count_waybills(projectfolder) + 1
        waybill_number = "{}_{:0>4}"\
            .format(str(projectnumber), next_waybill_number)
        filename = "{}.{}".format(waybill_number, self.__extension)
        with open(exportfolder / filename, "w") as f:
            f.write("{:>79}".format("Szállítólevél száma: {}\n"\
                                    .format(waybill_number)))
            f.write(textrep.waybill_header(projectnumber=projectnumber))
            for idx, item in enumerate(items):
                f.write(f"{idx+1:0>3}.    {item.withdraw_view}")
                f.write("\n")
            f.write(textrep.waybill_footer())
        logging.info(f"withdraw: {socket.gethostname()} {waybill_number}")

    def _get_exportfolder(self, projectnumber:Projectnumber) -> pathlib.Path:
        """Identify an existing or create a new folder for this export."""
        d = date.today()
        year = d.strftime("%Y")
        month = d.strftime("%B").capitalize()
        projectfolder = self.__waybillfolder / str(projectnumber)
        exportfolder = projectfolder / year / month
        for folder in self.__waybillfolder.iterdir():  # check existing folder
            if folder.is_dir():
                foldernumber = Projectnumber(folder.name)
                if foldernumber == projectnumber:
                    exportfolder = folder / year / month
                    break
        os.makedirs(exportfolder, exist_ok=True)
        return exportfolder

    def _count_waybills(self, projectfolder:pathlib.Path) -> int:
        return sum([len(files) for r, d, files in os.walk(projectfolder)])