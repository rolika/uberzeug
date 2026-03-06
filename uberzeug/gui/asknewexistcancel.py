from tkinter import *
from tkinter import ttk
from tkinter import simpledialog


class _AskNewExistCancel(simpledialog.Dialog):
    def __init__(self, parent:Widget) -> None:
        self.__answer = None
        super().__init__(parent, title="Figyelj!")

    def body(self, parent:Widget) -> None:
        ttk.Label(self, text="Már létezik anyag ilyen névvel és egységárral.").pack(ipadx=5, ipady=5, padx=5, pady=5)

    def buttonbox(self) -> None:
        box = Frame(self)
        ttk.Button(box, text="Új tétel legyen!", command=self._newitem).pack(ipadx=5, ipady=5, padx=5, pady=5, fill=X)
        ttk.Button(box, text="Meglévő tételhez adom.", command=self._existitem).pack(ipadx=5, ipady=5, padx=5, pady=5, fill=X)
        ttk.Button(box, text="Mégse", command=self.cancel).pack(ipadx=5, ipady=5, padx=5, pady=5, fill=X)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def _newitem(self, event:Event=None) -> None:
        self.__answer = "new"
        self.ok()

    def _existitem(self, event:Event=None) -> None:
        self.__answer = "exist"
        self.ok()

    @property
    def answer(self) -> str|None:
        return self.__answer


def ask_newexistcancel(parent:Widget=None) -> str|None:
    question = _AskNewExistCancel(parent)
    return question.answer


if __name__ == "__main__":
    print(ask_newexistcancel())