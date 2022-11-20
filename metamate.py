# Python 3.9.2

from enum import Enum
from glob import glob
from os import stat, path, rename
from time import strftime, localtime
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class Tag(Enum):
    SIZE = 6
    ACCESS = 7
    MODIFICATION = 8
    CREATION = 9

class Sep(Enum):
    UNDERSCORE = "_"
    DASH = "-"
    DOT = "."
    SPACE = " "

optionsTag = {"Creation Date": Tag.CREATION, "Modification Date": Tag.MODIFICATION, "Access Date": Tag.ACCESS, "Size": Tag.SIZE}
optionsSep = {"_": Sep.UNDERSCORE, "-": Sep.DASH, ".": Sep.DOT, " ": Sep.SPACE}

# setting appearance and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):

    # window dimensions
    X = 800
    Y = 440

    def __init__(self):

        super().__init__()

        # configure window
        self.title("metamate")
        self.minsize(self.X, self.Y)
        self.maxsize(self.X, self.Y)
        self.geometry(f"{self.X}x{self.Y}")
        
        # create 10x2 grid system
        self.grid_rowconfigure([e for e in range(10)], weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # variables
        self.variablePth = ctk.StringVar(self)
        self.variableTag = ctk.StringVar(self)
        self.variableSep = ctk.StringVar(self)

        # entry path
        self.path = ctk.CTkEntry(
            placeholder_text="/", width=600, height=40, corner_radius=20, textvariable=self.variablePth)
        self.path.grid(row=2, column=0, columnspan=2, padx=50)

        # button browse
        self.browse = ctk.CTkButton(
            text="Browse", width= 600, height=40, corner_radius=20, command=self.directory)
        self.browse.grid(row=3, column=0, columnspan=2, padx=50)

        # option-menu tag
        self.tag = ctk.CTkOptionMenu(
            width=280, height=40, button_color="#11B384", button_hover_color="#0D8A66", variable=self.variableTag, values=list(optionsTag.keys()), corner_radius=20)
        self.tag.set(list(optionsTag)[0])
        self.tag.grid(row=4, column=0, padx=20, sticky="e")

        # option-menu seperator
        self.sep = ctk.CTkOptionMenu(
            width=280, height=40, button_color="#11B384", button_hover_color="#0D8A66", variable=self.variableSep, values=list(optionsSep.keys()), corner_radius=20)
        self.sep.set(list(optionsSep)[0])
        self.sep.grid(row=4, column=1, padx=20, sticky="w")

        # button confirm
        self.ok = ctk.CTkButton(
            text="Go", width=140, height=40, corner_radius=20, command=self.renameDirectory)
        self.ok.grid(row=6, columnspan=2)

    # open explorer
    def directory(self):
        pth = filedialog.askdirectory()
        if pth:
            self.path.delete(0, ctk.END)
            self.path.insert(0, pth)
    
    # generate information and initialise renaming
    def renameDirectory(self):
        self.renameFiles(files=glob(f"{self.variablePth.get()}/*"), tag=optionsTag[self.variableTag.get()], sep=optionsSep[self.variableSep.get()])

    # renaming
    def renameFiles(self, files: list, tag: Tag, sep: Sep):
        for file in files:
            try:
                pass
            except:
                print("File not found")

            old = path.realpath(file)
            root, ext = path.splitext(old)
            meta = stat(file)

            if(tag == tag.SIZE):
                appendix = f"{meta[tag.value]}Byte"
            elif(tag in (tag.ACCESS, tag.MODIFICATION, tag.CREATION)):
                raw = meta[tag.value]
                time = localtime(raw)
                appendix = strftime("%Y-%m-%d", time)
            else:
                print("No tag defined")
                return

            new = f"{root}{sep.value}{appendix}{ext}"
            print(f"Old:\t{old}\nNew:\t{new}")
            rename(old, new)


if __name__ == "__main__":
    app = App()
    app.mainloop()
