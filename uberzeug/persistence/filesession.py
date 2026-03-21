from datetime import date
import os
import pathlib
from typing import List

import numpy as np
import pandas as pd

import utils.constants as ct
from utils import textrep
from utils.constants import *
from utils.projectnumber import Projectnumber
from record.logrecord import LogRecord
from record.stockitemrecord import TRANSLATE_ATTRIBUTES, StockItemRecord


class FileSession:
    """Class for handling file operations.
    This inventory uses file handling in one way as writing only.
    One can export the stock or its selected items, and a waybill will be
    exported whenever the stock is changed.
    The waybill exports come to project folder divided into years and months,
    like: 24_001 -> 2024 -> June.
    The waybill has a number which looks like 24_001_12, the latter being a
    serial number, which is always +1 of all waybills in the projectfolder."""
    def __init__(self, waybillfolder:str, turnoverfolder:str, stockfolder:str,
                 shortagefolder:str, extension:str=EXTENSION) -> None:
        self.__waybillfolder = pathlib.Path(waybillfolder)
        self.__turnoverfolder = pathlib.Path(turnoverfolder)
        self.__stockfolder = pathlib.Path(stockfolder)
        self.__shortagefolder = pathlib.Path(shortagefolder)
        self.__extension = extension
        os.makedirs(self.__waybillfolder, exist_ok=True)
        os.makedirs(self.__turnoverfolder, exist_ok=True)
        os.makedirs(self.__stockfolder, exist_ok=True)
        os.makedirs(self.__shortagefolder, exist_ok=True)

    def export_waybill(self, items:List[StockItemRecord],
                       projectnumber:Projectnumber) -> str:
        exportfolder = self._get_waybillexport_folder(projectnumber)
        projectfolder = pathlib.Path("/".join(exportfolder.parts[:-2]))
        next_waybill_number = self._count_files(projectfolder) + 1
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

    def export_turnover(self, projectnumber:str, yearmonth:str,
                        items:List[LogRecord], total:float,
                        lookup_term:str=None) -> None:
        if projectnumber != ct.SHOW_ALL:
            projectnumber = str(Projectnumber(projectnumber))
        exportfolder = self._get_turnoverexport_folder(projectnumber, yearmonth)
        nth_export = self._count_files(exportfolder) + 1
        filename:str = f"{projectnumber}_{nth_export}"
        if lookup_term:
            filename += f"_{lookup_term}"
        filename += f".{self.__extension}"
        with open(exportfolder / filename, "w") as f:
            f.write(textrep.turnover_header(projectnumber, yearmonth,
                                            lookup_term))
            for item in items:
                f.write(f"{item.listview}\n")
            f.write(textrep.turnover_footer(total))

    def export_stock(self, items:List[StockItemRecord], total:float=0.0,
                     lookup_term:str=None) -> None:
        filename = f"készlet_{date.today().strftime('%Y%m%d')}"
        if lookup_term:
            filename += f"_{lookup_term}"
        nth_export = self._count_files(self.__stockfolder) + 1
        filename += f"_{nth_export}"
        filename += f".{self.__extension}"
        with open(self.__stockfolder / filename, "w") as f:
            f.write(textrep.stock_header(lookup_term))
            for item in items:
                f.write(f"{item.valueview}\n")
            f.write(textrep.stock_footer(total))

    def _get_waybillexport_folder(self,
                                  projectnumber:Projectnumber) -> pathlib.Path:
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

    def _get_turnoverexport_folder(self, projectnumber:str,
                                   yearmonth:str) -> pathlib.Path:
        year = yearmonth.split(".")[0]
        month = yearmonth.split(".")[1].strip()
        exportfolder = self.__turnoverfolder  / projectnumber / year / month
        os.makedirs(exportfolder, exist_ok=True)
        return exportfolder

    def _count_files(self, folder:pathlib.Path) -> int:
        return sum([len(files) for r, d, files in os.walk(folder)])

    def export_shortages(self, items:List[StockItemRecord]) -> str:
        datalist = np.array([(item.name, item.stock, item.unit)\
                             for item in items])
        df = pd.DataFrame(datalist)
        filename = f"shortage_warning_{date.today().isoformat()}.xlsx"
        df.to_excel(self.__shortagefolder / filename, index=False)
        return filename
