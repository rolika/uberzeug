import locale
locale.setlocale(locale.LC_ALL, "")

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from uberzeug.gui.asklocalfloat import ask_localfloat
from uberzeug.gui.itemlistbox import ItemListbox
from uberzeug.gui.waybillpanel import WaybillPanel
from uberzeug._helper.constants import *
from uberzeug._helper.projectnumber import Projectnumber
from uberzeug.record.stockitemrecord import StockItemRecord


class _StockChangeDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, master_list:List[StockItemRecord],
                 projectnumber:Projectnumber, title:str, mode:Mode) -> None:
        self.__master_list = master_list
        self.__withdraw_list:List[StockItemRecord] = []
        self.__temp_list:List[StockItemRecord] = []
        self.__mode = mode
        if projectnumber:
            self.__title = f"{projectnumber.legal}: {title}"
        else:
            self.__title = title
        super().__init__(root, title=self.__title)

    def body(self, root:Widget) -> Widget:
        """Create dialog body. Return widget that should have initial focus."""
        box = Frame(self)
        self.__itemlistbox = ItemListbox(box, master_list=self.__master_list)
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__itemlistbox.bind_selection(self._stockchange)
        if self.__mode == Mode.DELETE:
            self.__waybillpanel = WaybillPanel(root=box,
                                               title=DELETE_TITLE,
                                               temp_list=self.__temp_list,
                                               itemlistbox=self.__itemlistbox)
        else:
            self.__waybillpanel = WaybillPanel(root=box,
                                               temp_list=self.__temp_list,
                                               itemlistbox=self.__itemlistbox)
        self.__waybillpanel.pack(padx=PADX, pady=PADY)
        box.pack()
        return self.__itemlistbox.lookup_entry

    def buttonbox(self):
        """Override standard button texts."""
        box = Frame(self)
        w = ttk.Button(box, text="KÉSZ", width=10, command=self.ok,
                       default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Mégse", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def apply(self) -> None:
        self.__withdraw_list = self.__temp_list

    def _stockchange(self, _:Event) -> None:
        item = self.__itemlistbox.get_record()
        if self.__mode == Mode.DEPOSIT:
            initvalue = None
            maxvalue = None
            sign = 1
        elif self.__mode == Mode.DELETE:
            setattr(item, "change", -(item.stock))
            item.stock = 0.0
            self.__itemlistbox.delete_item(item)
            self.__temp_list.append(item)
            self.__waybillpanel.update_waybill()
            return
        else:
            initvalue = item.stock
            maxvalue = item.stock
            sign = -1
        change = ask_localfloat(title=self.__title, prompt=item.name, root=self,
                                initvalue=initvalue, minvalue=0,
                                maxvalue=maxvalue, unit=item.unit,
                                packaging=item.packaging)
        already_withdrawed = False
        if change:
            for withdrawed in self.__temp_list:
                if withdrawed.articlenumber == item.articlenumber:
                    already_withdrawed = True
                    break  # there can be only one
            if already_withdrawed:
                withdrawed.undo_change()
                withdrawed.change += (sign * change)
                withdrawed.apply_change()
                if self.__mode != Mode.DEPOSIT:
                    self.__itemlistbox.update_item(withdrawed)
            else:
                setattr(item, "change", sign * change)
                item.apply_change()
                self.__temp_list.append(item)
                if self.__mode != Mode.DEPOSIT:
                    self.__itemlistbox.update_item(item)
            self.__waybillpanel.update_waybill()

    @property
    def withdraw_list(self) -> List[StockItemRecord]|None:
        return self.__withdraw_list


def withdraw_dialog(root:Widget, master_list:List[StockItemRecord],
                    projectnumber:Projectnumber) -> List[StockItemRecord]|None:
    withdrawed_items = _StockChangeDialog(root, master_list, projectnumber,
                                          WITHDRAW_TITLE, Mode.WITHDRAW)
    return withdrawed_items.withdraw_list


def takeback_dialog(root:Widget, master_list:List[StockItemRecord],
                    projectnumber:Projectnumber) -> List[StockItemRecord]|None:
    takeback_items = _StockChangeDialog(root, master_list, projectnumber,
                                        TAKEBACK_TITLE, Mode.TAKEBACK)
    return takeback_items.withdraw_list


def deposit_dialog(root:Widget, master_list:List[StockItemRecord])\
    -> List[StockItemRecord]|None:
    deposit_items = _StockChangeDialog(root, master_list, None, DEPOSIT_TITLE,
                                       Mode.DEPOSIT)
    return deposit_items.withdraw_list


def delete_dialog(root:Widget, master_list:List[StockItemRecord])\
    -> List[StockItemRecord]|None:
    deposit_items = _StockChangeDialog(root, master_list, None,DELETE_TITLE,
                                       Mode.DELETE)
    return deposit_items.withdraw_list