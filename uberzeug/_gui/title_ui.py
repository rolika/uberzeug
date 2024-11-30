import os
from tkinter import *
from tkinter import ttk
from typing import List

from uberzeug._helper.constants import *
import uberzeug._helper.textrep as textrep


class TitleUI(Frame):
    def __init__(self, title:str, organization:List[str], root:Widget=None,
                 title_image:str=TITLE_IMAGE, **kwargs) -> None:
        super().__init__(**kwargs)
        if os.name == "posix":
            icon = PhotoImage(file = LINUX_ICON)
            self.master.tk.call("wm", "iconphoto", self.master._w, icon)
        else:
            self.master.iconbitmap(default = WINDOWS_ICON)
        self.master.title(textrep.explode(title, width=3))
        self.__company = organization[0]
        self.__title_image = PhotoImage(file=title_image)
        self._body()

    def _body(self) -> None:
        box = LabelFrame(self, text=self.__company, labelanchor=N)
        canvas = Canvas(box, width=640, height=295)
        canvas.create_image(0, 0, image=self.__title_image, anchor=NW)
        canvas.pack(padx=5, pady=5)
        box.pack(padx=5, pady=5)
        box = ttk.LabelFrame(self, text="Anyagok kezelése")
        self.__newitem_button = ttk.Button(box, text="Új anyag")
        self.__newitem_button.pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Meglévő anyag módosítása",
                   state=DISABLED).pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Anyag törlése", state=DISABLED)\
            .pack(fill=X, padx=5, pady=5)
        box.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
        box = ttk.LabelFrame(self, text="Raktárkészlet-kezelés")
        self.__withdraw_button =ttk.Button(box, text="Kivét projektre")
        self.__withdraw_button.pack(fill=X, padx=5, pady=5)
        self.__takeback_button =ttk.Button(box, text="Visszavét projektről")
        self.__takeback_button.pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Raktárkészlet exportálása", state=DISABLED)\
            .pack(fill=X, padx=5, pady=5)
        box.pack(fill=BOTH, padx=5, pady=5)

    @property
    def withdraw_button(self) -> ttk.Button:
        return self.__withdraw_button

    @withdraw_button.setter
    def withdraw_button(self, command:callable) -> None:
        self.__withdraw_button["command"] = command

    @property
    def takeback_button(self) -> ttk.Button:
        return self.__takeback_button

    @takeback_button.setter
    def takeback_button(self, command:callable) -> None:
        self.__takeback_button["command"] = command

    @property
    def newitem_button(self) -> ttk.Button:
        return self.__newitem_button

    @takeback_button.setter
    def newitem_button(self, command:callable) -> None:
        self.__newitem_button["command"] = command


if __name__ == "__main__":
    app = Tk()
    titleui = TitleUI(app)
    titleui.pack()
    app.resizable(False, False)
    app.mainloop()
