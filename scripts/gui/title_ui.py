import os
from tkinter import *
from tkinter import ttk

TITLE_IMAGE = r"data/titleimg.gif"
WINDOWS_ICON = "data/pohlen.ico"
LINUX_ICON = "data/pohlen.gif"


class TitleUI(Frame):
    def __init__(self, root=None, title_image=TITLE_IMAGE, **kwargs) -> None:
        super().__init__(**kwargs)
        if os.name == "posix":
            icon = PhotoImage(file = LINUX_ICON)
            self.master.tk.call("wm", "iconphoto", self.master._w, icon)
        else:
            self.master.iconbitmap(default = WINDOWS_ICON)
        self.master.title("Pohlen-Dach")
        self.__title_image = PhotoImage(file=title_image)
        self._body()

    def _body(self) -> None:
        box = LabelFrame(self, text="Raktárkészlet-kezelő alkalmazás",
                         labelanchor=N)
        canvas = Canvas(box, width=640, height=295)
        canvas.create_image(0, 0, image=self.__title_image, anchor=NW)
        canvas.pack(padx=5, pady=5)
        box.pack(padx=5, pady=5)
        box = ttk.LabelFrame(self, text="Anyagok kezelése")
        ttk.Button(box, text="Új anyag").pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Meglévő anyag módosítása")\
            .pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Anyag törlése").pack(fill=X, padx=5, pady=5)
        box.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
        box = ttk.LabelFrame(self, text="Raktárkészlet-kezelés")
        self.__withdraw_button =ttk.Button(box, text="Kivét projektre")
        self.__withdraw_button.pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Visszavét projektről")\
            .pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Új raktári tétel").pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Meglévő raktári tétel törlése")\
            .pack(fill=X, padx=5, pady=5)
        ttk.Button(box, text="Raktárkészlet exportálása")\
            .pack(fill=X, padx=5, pady=5)
        box.pack(fill=BOTH, padx=5, pady=5)
    
    @property
    def withdraw_button(self) -> ttk.Button:
        return self.__withdraw_button
    
    @withdraw_button.setter
    def withdraw_button(self, command:callable) -> None:
        self.__withdraw_button["command"] = command


if __name__ == "__main__":
    app = Tk()
    titleui = TitleUI(app)
    titleui.pack()
    app.resizable(False, False)
    app.mainloop()
