from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from scripts.gui import styles
from scripts.projectnumber import Projectnumber


class _AskProjectNumber(simpledialog.Dialog):
    """Ask for a valid project number."""
    def __init__(self, root=None) -> None:
        self.__projectnumber = None
        self.__entry_var = StringVar()
        super().__init__(root, title="Projekt")


    def body(self, root:Widget) -> Widget:
        is_valid = self.register(self._is_valid)
        box = Frame(self)
        ttk.Label(box, text="Kérlek, adj meg egy projektszámot:").pack()
        entry = ttk.Entry(box, justify=CENTER, textvariable=self.__entry_var, validate="all", validatecommand=(is_valid, "%P", "%W"))
        entry.pack()
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
        self.__projectnumber = Projectnumber(self.__entry_var.get())

    @property
    def projectnumber(self) -> Projectnumber:
        return self.__projectnumber

    def _is_valid(self, text:str, name:str) -> bool:
        projectnumber = Projectnumber(text)
        if bool(projectnumber):
            styles.apply_entry_ok(self, name)
            self.__ok_button["state"] = NORMAL
            self.bind("<Return>", self.ok)
            self.bind("<KP_Enter>", self.ok)
        else:
            styles.apply_entry_error(self, name)
            self.__ok_button["state"] = DISABLED
            self.unbind("<Return>")
            self.unbind("<KP_Enter>")
        return True


def ask_projectnumber(root:Widget=None):
    project = _AskProjectNumber(root)
    return project.projectnumber


if __name__ == "__main__":
    print(ask_projectnumber())