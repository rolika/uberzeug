import os
from tkinter import *
from tkinter import messagebox

from scripts.databasesession import DatabaseSession
from scripts.gui.controldevice import ControlDevice
from scripts.gui.itemlistbox import ItemListbox
from scripts.gui.stockitemform import StockItemForm
from scripts.stockitemrecord import StockItemRecord


PROGRAM = "Készlet-nyilvántartó"
WINDOWS_ICON = "data/pohlen.ico"
LINUX_ICON = "data/pohlen.gif"
MARKER_COLOR = ("green", "darkgreen")

PADX = 2
PADY = 2


class Gui(Frame):
    def __init__(self, root=None, version="0.0.0",
                 dbsession:DatabaseSession=None) -> None:
        super().__init__(root)
        if os.name == "posix":
            icon = PhotoImage(file = LINUX_ICON)
            self.master.tk.call("wm", "iconphoto", self.master._w, icon)
        else:
            self.master.iconbitmap(default = WINDOWS_ICON)
        self.master.title(PROGRAM + " v" + version)
        self.__dbsession = dbsession
        self._build_interface()
        self.pack(padx=PADX, pady=PADY)

    def _build_interface(self):
        frame = Frame(self)
        self.stockitemform = StockItemForm(frame)
        self.itemlistbox = ItemListbox(frame, dbsession=self.__dbsession)
        self.stockitemform.grid(row=0, column=0, padx=PADX, pady=PADY,
                                sticky=N+E+W)
        self.itemlistbox.grid(row=0, column=1, padx=PADX, pady=PADY,
                              sticky=N+S, rowspan=2)
        self.controldevice = ControlDevice(frame)
        self.controldevice.grid(row=1, column=0, padx=PADX, pady=PADY,
                                sticky=E+W+N+S)
        self.controldevice.set_newitem_command(self.stockitemform.clear)
        frame.pack()

    def update_form(self, item:StockItemRecord) -> None:
        self.stockitemform.populate(item)
    
    def check_item(self) -> StockItemRecord|None:
        """Before updating the database record, check if the form is valid and
        warn the user if the stock has changed."""
        if self.stockitemform.is_valid():
            original_item = self.itemlistbox.selected_item
            updated_item = self.stockitemform.retrieve()
            if original_item and updated_item.articlenumber and\
                original_item.stock != updated_item.stock:
                if messagebox.askokcancel(title="Vigyázz!",
                                          message="Felülírod a készletet?"):
                    return updated_item  # update
            else:
                return updated_item  # insert
        else:
            messagebox.showwarning(title="Hiányos adatok!",
                                   message="A piros mezőket javítsd!")
        return None


if __name__ == "__main__":
    import locale
    locale.setlocale(locale.LC_ALL, "")
    gui = Gui()
    test_list = [str(i) for i in range(50)]
    gui.itemlistbox.populate(test_list)
    gui.mainloop()
