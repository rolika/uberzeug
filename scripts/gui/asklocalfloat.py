import locale

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from scripts.gui import styles


class _AskLocalFloat(simpledialog.Dialog):
    """Ask for a float number and verify it considering locale settings."""
    def __init__(self, title:str, prompt:str, root:Widget=None, initvalue:float=None,
                 minvalue:float=None, maxvalue:float=None,
                 unit:str=None) -> None:
        self.__prompt = prompt
        self.__minvalue = minvalue
        self.__maxvalue = maxvalue
        self.__unit = unit
        self.__number = None
        self.__entry_var = StringVar()
        if initvalue:
            self.__entry_var.set(locale.format_string(f="%.2f", val=initvalue))
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        is_okay = self.register(self._is_okay)
        box = Frame(self)
        ttk.Label(box, text=self.__prompt).pack()
        entry = ttk.Entry(box, justify=RIGHT, textvariable=self.__entry_var,
                          validate="all", validatecommand=(is_okay, "%P", "%W"))
        entry.select_range(0, END)
        entry.pack(side=LEFT)
        ttk.Label(box, text=self.__unit).pack()
        box.pack()
        return entry

    def buttonbox(self):
        """Override standard button texts."""
        box = Frame(self)
        self.__ok_button = Button(box, text="OK", width=10,
                                  command=self.ok, default=ACTIVE)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        Button(box, text="Mégse", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self) -> None:
        self.__number = locale.atof(self.__entry_var.get())

    @property
    def number(self) -> float:
        return self.__number

    def _is_okay(self, text:str, name:str) -> bool:
        number = None
        try:
            number = locale.atof(text)
            if self.__minvalue is not None and (number < self.__minvalue):
                raise ValueError
            if self.__maxvalue is not None and (number > self.__maxvalue):
                raise ValueError
            styles.apply_entry_ok(self, name)
            self.__ok_button["state"] = NORMAL
            self.bind("<Return>", self.ok)
            self.bind("<KP_Enter>", self.ok)
        except ValueError:
            styles.apply_entry_error(self, name)
            self.__ok_button["state"] = DISABLED
            self.unbind("<Return>")
            self.unbind("<KP_Enter>")
        return True


def ask_localfloat(title:str, prompt:str, root:Widget=None,
                   initvalue:float=None, minvalue:float=None,
                   maxvalue:float=None, unit:str=None) -> float:
    float_ = _AskLocalFloat(title, prompt, root, initvalue, minvalue, maxvalue,
                            unit)
    return float_.number


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")
    print(ask_localfloat(title="Kivét", prompt="Mennyit veszel ki?", root=None,
                         initvalue=324.5, minvalue=10.0, maxvalue=500.0))