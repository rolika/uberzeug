from tkinter import *
from tkinter import ttk

from uberzeug.gui import styles
from uberzeug.itemrecord import ItemRecord


SHORT_FIELD = 8
MID_FIELD = 16
PADX = 3
PADY = 3
DEFAULT_PACKAGING = 0
DEFAULT_SHELFLIFE = 12


class ItemMask(LabelFrame):
    def __init__(self):
        super().__init__(text="Anyag")
        self._init_controll_variables()
        self._build_interface()

    def _init_controll_variables(self) -> None:
        self.__name_var = StringVar()
        self.__nickname_var = StringVar()
        self.__manufacturer_var = StringVar()
        self.__description_var = StringVar()
        self.__color_var = StringVar()
        self.__comment_var = StringVar()
        self.__unit_var = StringVar()
        self.__packaging_var = StringVar()
        self.__shelflife_var = StringVar()

    def _build_interface(self) -> None:
        is_number = self.register(self._is_number)
        is_empty = self.register(self._is_empty)
        Label(self, text="Megnevezés:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        self.__name_entry =\
            ttk.Entry(self, justify=LEFT, textvariable=self.__name_var,
                      name="name", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self.__name_entry.grid(row=0, column=1, sticky=E+W, padx=PADX,
                               pady=PADY, columnspan=6)
        self.__name_entry.focus()

        Label(self, text="Gyártó:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        self.__manufacturer_entry =\
            ttk.Entry(self, justify=LEFT, textvariable=self.__manufacturer_var,
                      name="manufacturer", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self.__manufacturer_entry.grid(row=1, column=1, sticky=E+W, padx=PADX,
                                      pady=PADY, columnspan=3)
        Label(self, text="Becenév:")\
            .grid(row=1, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__nickname_var)\
            .grid(row=1, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Leírás:")\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__description_var)\
            .grid(row=2, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=6)

        Label(self, text="Megjegyzés:")\
            .grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__comment_var)\
            .grid(row=3, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)
        Label(self, text="Szín:")\
            .grid(row=3, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__color_var)\
            .grid(row=3, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Kiszerelés:")\
            .grid(row=4, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                  textvariable=self.__packaging_var, name="packaging",
                  validate="all", validatecommand=(is_number, "%P", "%W"))\
                    .grid(row=4, column=1, sticky=W, padx=PADX, pady=PADY)
        self.__unit_entry =\
            ttk.Entry(self, width=SHORT_FIELD, justify=LEFT,
                      textvariable=self.__unit_var, name="unit", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self.__unit_entry.grid(row=4, column=2, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="egység")\
            .grid(row=4, column=3, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="Eltartható:")\
            .grid(row=4, column=4, sticky=E, padx=PADX, pady=PADY)
        self.__shelflife_entry =\
            ttk.Entry(self, width=MID_FIELD, justify=RIGHT,
                      textvariable=self.__shelflife_var, name="shelflife",
                      validate="all", validatecommand=(is_number, "%P", "%W"))
        self.__shelflife_entry.grid(row=4, column=5, sticky=W,
                                   padx=PADX, pady=PADY)
        Label(self, text="hónap")\
            .grid(row=4, column=6, padx=PADX, pady=PADY)
        self.__packaging_var.set(DEFAULT_PACKAGING)
        self.__shelflife_var.set(DEFAULT_SHELFLIFE)

    def retrieve(self) -> ItemRecord:
        return ItemRecord(
            name=self.__name_var.get(),
            nickname=self.__nickname_var.get(),
            manufacturer=self.__manufacturer_var.get(),
            description=self.__description_var.get(),
            color=self.__color_var.get(),
            comment=self.__comment_var.get(),
            unit=self.__unit_var.get(),
            packaging=self.__packaging_var.get(),
            shelflife=self.__shelflife_var.get()
        )

    def populate(self, item:ItemRecord) -> None:
        self.__name_var.set(item.name)
        self.__nickname_var.set(item.nickname)
        self.__manufacturer_var.set(item.manufacturer)
        self.__description_var.set(item.description)
        self.__color_var.set(item.color)
        self.__comment_var.set(item.comment)
        self.__unit_var.set(item.unit)
        self.__packaging_var.set(item.packaging)
        self.__shelflife_var.set(item.shelflife)
        self.__name_entry["style"] = "okstyle.TEntry"
        self.__manufacturer_entry["style"] = "okstyle.TEntry"
        self.__unit_entry["style"] = "okstyle.TEntry"
        self.__shelflife_entry["style"] = "okstyle.TEntry"

    def disable(self) -> None:
        for child in self.winfo_children():
            if type(child) is ttk.Entry:
                child["state"] = DISABLED

    def enable(self) -> None:
        for child in self.winfo_children():
            if type(child) is ttk.Entry:
                child["state"] = NORMAL

    def is_valid(self) -> bool:
        return styles.is_entry_ok(self)

    def _is_number(self, text:str, name:str) -> bool:
        try:
            number = float(text)
            if number >= 0:
                styles.apply_entry_ok(self, name)
        except ValueError:
            styles.apply_entry_error(self, name)
        return True

    def _is_empty(self, text:str, name:str) -> bool:
        if text:
            styles.apply_entry_ok(self, name)
        else:
            styles.apply_entry_error(self, name)
        return True

    @property
    def unit(self) -> str:
        return self.__unit_var.get()


if __name__ == "__main__":
    mask = ItemMask()
    mask.disable()
    mask.enable()
    mask.mainloop()
