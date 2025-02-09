import re
from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip
from typing import List

from utils.constants import *
from record.stockitemrecord import Record


class ItemListbox(LabelFrame):
    def __init__(self, root=None, title=STOCKNAME,
                 master_list:List[Record]=None) -> None:
        super().__init__(root, text=title)
        self.__master_list = master_list
        self.__display_list = None
        self._init_controll_variables()
        self._build_interface()
        self._bindings()
        self._clear_selection()

    def _init_controll_variables(self) -> None:
        self.__lookup_var = StringVar()

    def _build_interface(self) -> None:
        self.__lookup_entry = ttk.Entry(self, textvariable=self.__lookup_var,
                                        validate="key")
        Button(self, bitmap="questhead", command=self._clear_selection)\
            .grid(row=0, column=1)

        vertical_scroll = Scrollbar(self, orient=VERTICAL)
        self.__listbox = Listbox(self,
                                 cursor="hand2",
                                 font=("Liberation Mono", "-12"),
                                 selectmode=SINGLE,
                                 width=60,
                                 height=23,
                                 yscrollcommand=vertical_scroll.set,
                                 exportselection=False)
        vertical_scroll["command"]=self.__listbox.yview

        ToolTip(self.__listbox, msg=self._get_item_info, refresh=0.05)

        self.__lookup_entry.grid(row=0, column=0, sticky=E+W)
        self.__listbox.grid(row=1, column=0)
        vertical_scroll.grid(row=1, column=1, sticky=N+S)

    def _bindings(self) -> None:
        self.__listbox.bind("<Button-4>",
                            lambda _: self.__listbox.yview_scroll(-1, UNITS))
        self.__listbox.bind("<Button-5>",
                            lambda _: self.__listbox.yview_scroll(1, UNITS))
        self.__listbox.bind("<MouseWheel>",
            lambda e: self.__listbox.yview_scroll(int(e.delta / 120), UNITS))
        lookup = self.__listbox.register(self._lookup)
        self.__lookup_entry["validatecommand"] = (lookup, "%P")
        self.__listbox.bind("<Escape>", self._clear_selection)
        self.__lookup_entry.bind("<Escape>", self._clear_selection)
        self.__listbox.bind("<Motion>", self._on_mouse_motion, add="+")

    def _on_mouse_motion(self, event:Event) -> None:
        self._listbox_idx = self.__listbox.index(f"@{event.x}, {event.y}")

    def _get_item_info(self) -> str:
        try:
            return self.__display_list[int(self._listbox_idx)].tooltip_view
        except AttributeError:
            return ""
        except (IndexError, ValueError):
            return ""

    def _clear_selection(self, _=None) -> None:
        self.__lookup_var.set("")
        self._lookup("")
        self.__lookup_entry.focus()

    def _populate(self, item_list:List) -> None:
        self.__listbox.delete(0, END)
        self.__display_list = item_list
        for item in item_list:
            self.__listbox.insert(END, item.listview)

    def _lookup(self, term:str) -> bool:
        selection = self.__master_list
        for word in re.split(r"\W+", term.lower()):
            if word:
                selection = [item for item in selection if item.contains(word)]
        self._populate(selection)
        return True

    def _find_item_index(self, item:Record) -> int|None:
        for idx, stockitem in enumerate(self.__display_list):
            if stockitem.articlenumber == item.articlenumber:
                return idx
        return None

    def bind_selection(self, method:callable) -> None:
        self.__listbox.bind("<<ListboxSelect>>", method)

    def get_record(self) -> Record:
        try:
            return self.__display_list[self.__listbox.curselection()[0]]
        except IndexError:  # empty list
            return None

    def update_item(self, item:Record) -> None:
        idx = self._find_item_index(item)
        if idx is not None:
            self.__display_list[idx] = item
            self.__listbox.delete(idx)
            self.__listbox.insert(idx, str(item))
        else:
            self.__display_list.append(item)
            self.__listbox.insert(END, str(item))

    def delete_item(self, item:Record) -> None:
        idx = self._find_item_index(item)
        self.__display_list.pop(idx)
        self.__listbox.delete(idx)
    
    def set_width(self, width:int) -> None:
        self.__listbox.config(width=width)

    @property
    def lookup_entry(self) -> ttk.Entry:
        return self.__lookup_entry

    @lookup_entry.setter
    def lookup_entry(self, value:str) -> None:
        self.__lookup_var.set(value)


if __name__ == "__main__":
    itemlist = ItemListbox()
    itemlist.grid()
    itemlist.mainloop()