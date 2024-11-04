from tkinter import *
from tkinter import ttk


PADX = 2
PADY = 2


class ControlDevice(LabelFrame):
    def __init__(self, root=None) -> None:
        super().__init__(root, text="Kezelőgombok")
        self._build_interface()
    
    def _build_interface(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        item = LabelFrame(self, text="Tétel")
        self.__newitem_button = ttk.Button(item, text="Új")
        self.__saveitem_button = ttk.Button(item, text="Mentés")
        self.__newitem_button.grid(row=0, column=0, padx=PADX, pady=PADY)
        self.__saveitem_button.grid(row=1, column=0, padx=PADX, pady=PADY)

        waybill = LabelFrame(self, text="Szállítólevél")
        self.__withdraw_button = ttk.Button(waybill, text="Kivét")
        self.__takeback_button = ttk.Button(waybill, text="Visszavét")
        self.__deposit_button = ttk.Button(waybill, text="Bevét")
        self.__exportwaybill_button = ttk.Button(waybill, text="Export")
        self.__withdraw_button.grid(row=0, column=0, padx=PADX, pady=PADY)
        self.__takeback_button.grid(row=0, column=1, padx=PADX, pady=PADY)
        self.__deposit_button.grid(row=0, column=2, padx=PADX, pady=PADY)
        self.__exportwaybill_button.grid(row=1, column=1, padx=PADX, pady=PADY)

        item.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+N+S)
        waybill.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=E+N+S)
    
    def set_newitem_command(self, func:callable) -> None:
        self.__newitem_button["command"] = func
    
    def set_saveitem_command(self, func:callable) -> None:
        self.__saveitem_button["command"] = func
    
    def set_withdraw_command(self, func:callable) -> None:
        self.__withdraw_button["command"] = func