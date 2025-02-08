from tkinter import *
from tkinter import ttk


class ControllUI(Frame):
    def __init__(self, root:Widget=None, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._body()

    def _body(self) -> None:
        box = ttk.Frame(self)
        self.__controlling_button = ttk.Button(box, text="Utókalkuláció")
        self.__controlling_button.pack(fill=BOTH, padx=5, pady=5, side=LEFT)
        self.__transfer_button = ttk.Button(box, text="Átkönyvelés")
        self.__transfer_button.pack(fill=BOTH, padx=5, pady=5, side=LEFT)
        self.__export_button = ttk.Button(box, text="Raktárkészlet\nexportálása")
        self.__export_button.pack(fill=BOTH, padx=5, pady=5, side=LEFT)
        box.pack(side=LEFT, padx=5, pady=5, anchor=NW)

    @property
    def controlling_button(self) -> ttk.Button:
        return self.__controlling_button

    @controlling_button.setter
    def controlling_button(self, command:callable) -> None:
        self.__controlling_button["command"] = command

    @property
    def transfer_button(self) -> ttk.Button:
        return self.__transfer_button

    @transfer_button.setter
    def transfer_button(self, command:callable) -> None:
        self.__transfer_button["command"] = command

    @property
    def export_button(self) -> ttk.Button:
        return self.__export_button

    @export_button.setter
    def export_button(self, command:callable) -> None:
        self.__export_button["command"] = command


if __name__ == "__main__":
    app = Tk()
    titleui = ControllUI(app)
    titleui.pack()
    app.mainloop()