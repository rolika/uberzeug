import locale
locale.setlocale(locale.LC_ALL, "")

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from uberzeug._gui.asklocalfloat import ask_localfloat
from uberzeug._gui.itemlistbox import ItemListbox
from uberzeug._gui.waybillpanel import WaybillPanel
from uberzeug._helper.projectnumber import Projectnumber
from uberzeug._record.stockitemrecord import StockItemRecord


PADX = 2
PADY = 2


class _WithdrawDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, master_list:List[StockItemRecord],
                 projectnumber:Projectnumber) -> None:
        self.__master_list = master_list
        self.__withdraw_list:List[StockItemRecord] = []
        self.__temp_list:List[StockItemRecord] = []
        super().__init__(root, title=f"{projectnumber.legal}: Kivét raktárból")

    def body(self, root:Widget) -> None:
        """Create dialog body. Return widget that should have initial focus."""
        box = Frame(self)
        self.__itemlistbox = ItemListbox(box, master_list=self.__master_list)
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__itemlistbox.bind_selection(self._withdraw)
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

    def _withdraw(self, _:Event) -> float:
        item = self.__itemlistbox.get_record()
        change = ask_localfloat(title="Kivét", prompt=item.name, root=self,
                                initvalue=item.stock, minvalue=0,
                                maxvalue=item.stock, unit=item.unit)
        if change:
            setattr(item, "change", -change)
            item.apply_change()
            self.__temp_list.append(item)
            self.__itemlistbox.update_item(item)
            self.__waybillpanel.update_waybill()

    @property
    def withdraw_list(self) -> List[StockItemRecord]|None:
        return self.__withdraw_list


def withdraw_dialog(root:Widget, master_list:List[StockItemRecord],
                    projectnumber:Projectnumber) -> List[StockItemRecord]|None:
    withdrawed_items = _WithdrawDialog(root, master_list, projectnumber)
    return withdrawed_items.withdraw_list