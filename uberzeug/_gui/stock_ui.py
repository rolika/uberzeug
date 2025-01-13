import os
from tkinter import *
from tkinter import ttk
from typing import List

from uberzeug._helper import textrep


class StockUI(Frame):
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
        box = ttk.LabelFrame(self, text="Anyagok kezelése")
        self.__newitem_button = ttk.Button(box, text="Új anyag")
        self.__newitem_button.pack(fill=X, padx=5, pady=5)
        self.__modify_button =ttk.Button(box, text="Meglévő anyag módosítása")
        self.__modify_button.pack(fill=X, padx=5, pady=5)
        self.__delete_button = ttk.Button(box, text="Anyag törlése")
        self.__delete_button.pack(fill=X, padx=5, pady=5)
        box.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
        box = ttk.LabelFrame(self, text="Raktárkészlet-kezelés")
        self.__withdraw_button =ttk.Button(box, text="Kivét projektre")
        self.__withdraw_button.pack(fill=X, padx=5, pady=5)
        self.__takeback_button = ttk.Button(box, text="Visszavét projektről")
