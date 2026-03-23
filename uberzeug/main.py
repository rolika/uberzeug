"""
ÜBERZEUG
"""


import configparser
import locale
locale.setlocale(locale.LC_ALL, "")
import logging
import socket
from tkinter import messagebox, simpledialog
from typing import List

from utils.constants import *
from gui.asknewexistcancel import ask_newexistcancel
from gui.askprojectnumber import ask_projectnumber
from gui.existingitemdialig import ExistingItemDialog
from gui.turnoverdialog import TurnoverDialog
from gui.modifyitemdialog import modifyitem_dialog
from gui.shortagewarningdialog import ShortageWarningDialog
from gui.stockitemdialog import stockitem_dialog
from gui.title_ui import TitleUI
from gui.stockchangedialog\
    import delete_dialog, deposit_dialog, takeback_dialog, withdraw_dialog
from gui.stockexportdialog import StockExportDialog
from persistence.databasesession import DatabaseSession
from persistence.filesession import FileSession


class Uberzeug():
    def __init__(self, title:str=APPLICATION_TITLE,
                 organization:List[str]=ORGANIZATION) -> None:

        config = configparser.ConfigParser()
        config.read(CONFIGFILE)
        database_file = config["DEFAULT"]["database"]
        waybillfolder = config["DEFAULT"]["waybillfolder"]
        turnoverfolder = config["DEFAULT"]["turnoverfolder"]
        stockfolder = config["DEFAULT"]["stockfolder"]
        logfile = config["DEFAULT"]["logfile"]
        title_image = config["DEFAULT"]["title_image"]
        windows_icon = config["DEFAULT"]["windows_icon"]
        linux_icon = config["DEFAULT"]["linux_icon"]
        lookback_days = int(config["DEFAULT"]["lookback_days"])
        shortagefolder = config["DEFAULT"]["shortagefolder"]

        self.__dbsession = DatabaseSession(database_file)
        self.__filesession = FileSession(waybillfolder, turnoverfolder,
                                         stockfolder, shortagefolder)
        self.__ui = TitleUI(title, organization, title_image, windows_icon,
                            linux_icon, root=self)
        self.__lookback_days = lookback_days
        self._bindings()
        self._update_buttons()
        self.__ui.pack()
        logging.basicConfig(filename=logfile, encoding='utf-8',
                            format="%(levelname)s: %(asctime)s %(message)s",
                            datefmt="%Y.%m.%d %H:%M:%S", level=logging.INFO)
        self.__ui.mainloop()

    def _bindings(self) -> None:
        self.__ui.stockui.withdraw_button = self._withdraw
        self.__ui.stockui.takeback_button = self._takeback
        self.__ui.stockui.deposit_button = self._deposit
        self.__ui.stockui.newitem_button = self._newitem
        self.__ui.stockui.modify_button = self._modify
        self.__ui.stockui.delete_button = self._delete
        self.__ui.controllui.controlling_button = self._controlling
        self.__ui.controllui.export_button = self._export
        self.__ui.controllui.shortage_button = self._check_shortages

    def _withdraw(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        master_list = self.__dbsession.load_withdrawable_items()
        withdrawed_items = withdraw_dialog(self.__ui, master_list,
                                           projectnumber)
        if len(withdrawed_items):
            self.__dbsession.log_stock_change(withdrawed_items, projectnumber)
            waybill_number = self.__filesession.export_waybill(withdrawed_items,
                                                               projectnumber)
            logging.info(f"{socket.gethostname()} withdraw: {waybill_number}")
            messagebox.showinfo(WITHDRAW_TITLE,
                                WAYBILL_TITLE + " száma: " + waybill_number)

    def _takeback(self) -> None:
        projectnumber = ask_projectnumber(self.__ui)
        if not projectnumber:
            return
        master_list = self.__dbsession.get_project_stock(projectnumber)
        takeback_items = takeback_dialog(self.__ui, master_list, projectnumber)
        if len(takeback_items):
            for takeback in takeback_items:
                takeback.stock = takeback.backup_stock
                takeback.change = abs(takeback.change)
                takeback.apply_change()
            self.__dbsession.log_stock_change(takeback_items, projectnumber)
            waybill_number = self.__filesession.export_waybill(takeback_items,
                                                               projectnumber)
            logging.info(f"{socket.gethostname()} takeback: {waybill_number}")
            messagebox.showinfo(TAKEBACK_TITLE,
                                WAYBILL_TITLE + " száma: " + waybill_number)

    def _deposit(self) -> None:
        master_list = self.__dbsession.load_all_items()
        deposit_items = deposit_dialog(self.__ui, master_list)
        pieces = len(deposit_items)
        if pieces:
            self.__dbsession.update_stock(deposit_items)
            logging.info(f"{socket.gethostname()} deposit: {pieces} items")
            messagebox.showinfo(DEPOSIT_TITLE, f"{pieces} tétel bevételezve.")

    def _newitem(self) -> None:
        newitem = stockitem_dialog(self.__ui, "Új raktári tétel")
        host = socket.gethostname()
        update = False
        if newitem:
            log = f"new: {newitem.name} {newitem.stock} {newitem.unit}"
            message = f"új anyag: {newitem.name} {newitem.stock} {newitem.unit}"
            similar_items = self.__dbsession.lookup(newitem)
            if similar_items:
                existsdialog = ExistingItemDialog(self.__ui, "Hasonló anyagok",
                                                  newitem, similar_items)
                selected_item = existsdialog.selected_item
                if selected_item is None:  # cancel
                    return
                elif selected_item.articlenumber is not None:  # existing item
                    update = True
                    selected_item.stock += newitem.stock
                    log = f"update: {selected_item.name} + {newitem.stock} " +\
                          f"{newitem.unit}"
                    message = f"{selected_item.name} készletének növelése: " +\
                              f"+ {newitem.stock} {selected_item.unit}"
            if update:
                self.__dbsession.update(selected_item)
            else:
                self.__dbsession.insert(newitem)
            logging.info(f"{host} {log}")
            messagebox.showinfo("Felvéve a raktárba", message)
        self._update_buttons()

    def _modify(self) -> None:
        master_list = self.__dbsession.load_all_items()
        item = modifyitem_dialog(self.__ui, master_list)
        if item:
            old_item = self.__dbsession\
                .get_stockitem_by_articlenumber(item.articlenumber)
            space = " " if old_item.manufacturer else ""
            name = old_item.manufacturer + space + old_item.name
            setattr(item, "oldname", name)
            self.__dbsession.update(item)
            logging.info\
                (f"{socket.gethostname()} modify: {item.name} {item.stock}")
            messagebox.showinfo(MODIFIY_TITLE,
                f"{item.name} {item.stock} {item.unit}")

    def _delete(self) -> None:
        master_list = self.__dbsession.load_all_items()
        items = delete_dialog(self.__ui, master_list)
        if len(items) and\
            messagebox.askokcancel(DELETE_TITLE, "Biztos vagy benne?"):
            for item in items:
                self.__dbsession.delete(item)
                logging.info\
                (f"{socket.gethostname()} delete: {item.name} {-item.change}")
            messagebox.showinfo(DELETE_TITLE, "Anyag(ok) törölve.")
        self._update_buttons()

    def _update_buttons(self) -> None:
        empty_db = not len(self.__dbsession.load_all_items())
        self.__ui.stockui.switch_button_state(empty_db)

    def _controlling(self) -> None:
        TurnoverDialog(self.__ui, self.__dbsession, self.__filesession,
                       "Kontrolling")

    def _export(self) -> None:
        dialog:simpledialog.Dialog = StockExportDialog(self.__ui,
            "Készlet exportálása",
            self.__dbsession.select_all_items_for_export())
        if len(dialog.selected_records):
            filename =self.__filesession.export_stock(dialog.selected_records,
                                                      dialog.total_value,
                                                      dialog.lookup_term)
            messagebox.showinfo("Készlet exportálása", filename)

    def _check_shortages(self) -> None:
        short_items = []
        for item in self.__dbsession.get_usage(self.__lookback_days):
            prediction =\
                round(item.deliverytime * item.usage / self.__lookback_days)
            if item.stock < prediction:
                short_items.append(item)
        if short_items:
            ShortageWarningDialog(self.__ui, "Kifogyó készlet",
                                  self.__lookback_days, short_items,
                                  self.__filesession)
        else:
            messagebox.showinfo("Kifogyó készlet", "Nincs kifogyó készlet.")


if __name__ == "__main__":
    Uberzeug()