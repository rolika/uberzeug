from tkinter import *
from tkinter import ttk


class MainMenu(LabelFrame):
    """The main menu is a menubar in its own frame."""
    def __init__(self, root:Widget=None, **kwargs) -> None:
        super().__init__(root, text="Főmenü", **kwargs)
        self._body()

    def _body(self) -> None:
        self.__stockmenu = ttk.Menubutton(self, text="Raktár", width=10)
        self.__controllingmenu = ttk.Menubutton(self, text="Kontrolling",
                                                width=10)
        self.__projectmenu = ttk.Menubutton(self, text="Projektek", width=10)
        self.__helpmenu = ttk.Menubutton(self, text="Súgó", width=10)

        self.__stockmenu.pack(side=LEFT, padx=5, pady=5)
        self.__controllingmenu.pack(side=LEFT, padx=5, pady=5)
        self.__projectmenu.pack(side=LEFT, padx=5, pady=5)
        self.__helpmenu.pack(side=RIGHT, padx=5, pady=5)

