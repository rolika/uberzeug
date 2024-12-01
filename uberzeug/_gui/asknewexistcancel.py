from tkinter import *
from tkinter import simpledialog


class _AskNewExistCancel(simpledialog.Dialog):
    def __init__(self, parent:Widget) -> None:
        self.__answer = None
        super().__init__(parent, title="Figyelj!")
    
    def body(self, parent:Widget) -> None:
        Label(self, text="Már létezik anyag ilyen névvel és egységárral.").pack()
    
    def buttonbox(self) -> None:        
        box = Frame(self)
        Button(box, text="Új tétel legyen!", command=self._newitem).pack()
        Button(box, text="Meglévő tételhez adom.", command=self._existitem).pack()
        Button(box, text="Mégse", command=self.cancel).pack()
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