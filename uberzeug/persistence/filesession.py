from datetime import date, timedelta
import os
import pathlib
from typing import List

from utils import textrep
from utils.constants import *
from utils.projectnumber import Projectnumber
from record.stockitemrecord import StockItemRecord


class FileSession:
    """Class for handling file operations.
    This inventory uses file handling in one way as writing only.
    One can export the stock or its selected items, and a waybill will be
    exported whenever the stock is changed.
    The waybill exports come to project folder divided into years and months,
    like: 24_001 -> 2024 -> June.
    The waybill has a number which looks like 24_001_12, the latter being a
    serial number, which is always +1 of all waybills in the projectfolder."""
    def __init__(self, waybillfolder:str, turnoverfolder:str,
                  extension:str=EXTENSION) -> None:
        self.__waybillfolder = pathlib.Path(waybillfolder)
        self.__turnoverfolder = pathlib.Path(turnoverfolder)
        self.__extension = extension
        os.makedirs(self.__waybillfolder, exist_ok=True)
        os.makedirs(self.__turnoverfolder, exist_ok=True)

    def export_waybill(self, items:List[StockItemRecord],
                       projectnumber:Projectnumber) -> str:
        exportfolder = self._get_waybillexport_folder(projectnumber)
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
        return waybill_number

    def _get_waybillexport_folder(self, projectnumber:Projectnumber) -> pathlib.Path:
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

    def _get_turnoverexport_folder(self) -> pathlib.Path:
        """Always create a new year-previous month folder for turnover export,
        inside the turnover-folder, format: turnoverfolder/yyyy/mm"""
        d = date.today()
        prev = d.replace(day=1) - timedelta(days=1)
        year = prev.strftime("%Y")
        month = prev.strftime("%m")
        exportfolder = self.__turnoverfolder / year / month
        os.makedirs(exportfolder, exist_ok=True)
        return exportfolder

    def _count_waybills(self, projectfolder:pathlib.Path) -> int:
        return sum([len(files) for r, d, files in os.walk(projectfolder)])
