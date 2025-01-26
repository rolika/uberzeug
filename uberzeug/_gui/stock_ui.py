from tkinter import *
from tkinter import ttk


class StockUI(Frame):
    def __init__(self, root:Widget=None, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._body()

    def _body(self) -> None:
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
        self.__takeback_button.pack(fill=X, padx=5, pady=5)
        self.__deposit_button = ttk.Button(box, text="Bevételezés raktárba")
        self.__deposit_button.pack(fill=X, padx=5, pady=5)
        box.pack(fill=BOTH, padx=5, pady=5)

    def switch_button_state(self, empty_db:bool) -> None:
        state = "disabled" if empty_db else "normal"
        self.__withdraw_button["state"] = state
        self.__takeback_button["state"] = state
        self.__deposit_button["state"] = state
        self.__modify_button["state"] = state
        self.__delete_button["state"] = state

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
    def deposit_button(self) -> ttk.Button:
        return self.__deposit_button

    @takeback_button.setter
    def deposit_button(self, command:callable) -> None:
        self.__deposit_button["command"] = command

    @property
    def newitem_button(self) -> ttk.Button:
        return self.__newitem_button

    @takeback_button.setter
    def newitem_button(self, command:callable) -> None:
        self.__newitem_button["command"] = command

    @property
    def modify_button(self) -> ttk.Button:
        return self.__modify_button

    @modify_button.setter
    def modify_button(self, command:callable) -> None:
        self.__modify_button["command"] = command

    @property
    def delete_button(self) -> ttk.Button:
        return self.__delete_button

    @delete_button.setter
    def delete_button(self, command:callable) -> None:
        self.__delete_button["command"] = command


if __name__ == "__main__":
    app = Tk()
    titleui = StockUI(app)
    titleui.pack()
    app.mainloop()
