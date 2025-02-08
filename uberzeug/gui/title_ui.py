import os
from tkinter import *
from tkinter import ttk
from typing import List

from gui.controll_ui import ControllUI
import utils.textrep as textrep
from gui.stock_ui import StockUI


class TitleUI(Frame):
    def __init__(self, title:str, organization:List[str],
                 title_image:str, windows_icon:str, linux_icon:str,
                 root:Widget=None, **kwargs) -> None:
        super().__init__(**kwargs)
        if os.name == "posix":
            try:
                icon = PhotoImage(file = linux_icon)
                self.master.tk.call("wm", "iconphoto", self.master._w, icon)
            except TclError:
                pass
        else:
            try:
                self.master.iconbitmap(default = windows_icon)
            except TclError:
                pass
        self.master.title(textrep.explode(title, width=3))
        self.__company = organization[0]
        try:
            self.__title_image = PhotoImage(file=title_image)
        except TclError:
            self.__title_image = None
        self._body()

    def _body(self) -> None:
        box = LabelFrame(self, text=self.__company, labelanchor=N)
        canvas = Canvas(box, width=640, height=295)
        if self.__title_image:
            canvas.create_image(0, 0, image=self.__title_image, anchor=NW)
        canvas.pack(padx=5, pady=5)
        box.pack(padx=5, pady=5)
        self.__shortcut = ttk.Notebook(self)
        self.__stockui = StockUI(self.__shortcut)
        self.__stockui.pack(fill=BOTH, padx=5, pady=5)
        self.__controllui = ControllUI(self.__shortcut)
        self.__controllui.pack(fill=BOTH, padx=5, pady=5)
        self.__shortcut.add(self.__stockui, text="Raktár")
        self.__shortcut.add(self.__controllui, text="Kontrolling")
        self.__shortcut.add(ttk.Frame(self.__shortcut), text="Projektek")
        self.__shortcut.pack(fill=BOTH, padx=5, pady=5)

    @property
    def stockui(self) -> StockUI:
        return self.__stockui

    @property
    def controllui(self) -> ControllUI:
        return self.__controllui