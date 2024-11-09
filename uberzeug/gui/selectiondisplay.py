from tkinter import *


MID_FIELD = 16
PADX = 3
PADY = 3

ALL_SELECTED = "teljes raktár"


class SelectionDisplay(LabelFrame):
    def __init__(self):
        super().__init__(text="Kiválasztás")
        self._init_controll_variables()
        self._build_interface()

    def _init_controll_variables(self) -> None:
        self.__lookup_var = StringVar()
        self.__selectionvalue_var = StringVar()

    def _build_interface(self) -> None:
        Label(self, text="Kiválasztva:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        Label(self, textvariable=self.__lookup_var)\
            .grid(row=1, column=1, padx=PADX, pady=PADY)
        Label(self, text="Érték:")\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        Label(self, textvariable=self.__selectionvalue_var)\
            .grid(row=2, column=1, padx=PADX, pady=PADY)
        Label(self, text="Ft")\
            .grid(row=2, column=2, sticky=W, padx=PADX, pady=PADY)
    
    @property
    def lookup(self) -> str:
        return self.__lookup_var.get()
    
    @lookup.setter
    def lookup(self, value:str) -> None:
        if value:
            value = f"""\"{value}\""""
        else:
            value = ALL_SELECTED
        self.__lookup_var.set(value)
    
    @property
    def selectionvalue(self) -> str:
        return self.__selectionvalue_var.get()
    
    @selectionvalue.setter
    def selectionvalue(self, value:float) -> None:
        self.__selectionvalue_var.set(value)