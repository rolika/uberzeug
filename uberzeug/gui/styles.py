from tkinter import *
from tkinter import ttk

style = ttk.Style()
style.configure("okstyle.TEntry", fieldbackground="white")
style.configure("errorstyle.TEntry", fieldbackground="red")


def apply_entry_ok(widget:BaseWidget, widget_name:str) -> None:
    widget = widget.nametowidget(widget_name)
    widget["style"] = "okstyle.TEntry"


def apply_entry_error(widget:BaseWidget, widget_name:str) -> None:
    widget = widget.nametowidget(widget_name)
    widget["style"] = "errorstyle.TEntry"


def is_entry_ok(parent:BaseWidget) -> bool:
    for child in parent.winfo_children():
        if child.winfo_class() == "TEntry":
            if child["style"] == "errorstyle.TEntry":
                return False
    return True