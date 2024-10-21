import os
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

from scripts.gui.asklocalfloat import AskLocalFloat
from scripts.databasesession import DatabaseSession
from scripts.gui.itemlistbox import ItemListbox
from scripts.logrecord import LogRecord
from scripts.projectnumber import Projectnumber


PADX = 2
PADY = 2


class WithdrawUI(simpledialog.Dialog):
    def __init__(self, root:Widget, dbsession:DatabaseSession,
                 projectnumber:Projectnumber) -> None:
        self.__dbsession = dbsession
        self.__withdrawed_items = []
        self.__projectnumber = projectnumber
        super().__init__(root,
                         title=f"{self.__projectnumber.legal}: Kivét raktárból")
    
    def body(self, root:Widget) -> None:
        """Create dialog body. Return widget that should have initial focus."""
        box = Frame(self)
        self.__itemlistbox = ItemListbox(box, dbsession=self.__dbsession)
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__itemlistbox.populate(self.__dbsession.load_all_items())
        self.__itemlistbox.bind_selection(self._withdraw)
        box.pack()
        return self.__itemlistbox.lookup_entry

    def buttonbox(self):
        """Override standard button texts."""
        box = Frame(self)
        w = ttk.Button(box, text="KÉSZ", width=10, command=self.ok,
                       default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Mégse", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        box.pack()
    
    def _withdraw(self, _:Event) -> float:
        item = self.__itemlistbox.get_record()
        change = AskLocalFloat(title="Kivét", prompt=item.name, root=self,
                               initvalue=item.stock, minvalue=0,
                               maxvalue=item.stock, unit=item.unit)
        if change.number:
            setattr(item, "change", -change.number)
            setattr(item, "projectnumber", str(self.__projectnumber))
            self.__withdrawed_items.append(item)
            for item in self.__withdrawed_items:
                print(item.withdraw_view)
            print("---")