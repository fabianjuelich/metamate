"""
Dependencies:
Python 3.9.2
Python3-tk
CustomTkinter 4.6.3 (pip3)
icons8-m-96.png
"""

import os
import stat
import platform
from glob import glob
from enum import Enum
from time import strftime, localtime
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

class Tag(Enum):
    CREATION = 9
    MODIFICATION = 8
    ACCESS = 7
    SIZE = 6

class Sep(Enum):
    UNDERSCORE = "_"
    DASH = "-"
    DOT = "."
    SPACE = " "

# root directory for placeholder-text and safety
rootDir = os.path.abspath(os.sep)

# options
optionsTag = dict(zip(["Creation Date", "Modification Date", "Access Date", "Size"], list(Tag)))
optionsSep = dict(zip(["_", "-", ".", " "], list(Sep)))

# appearance and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("sweetkind")

class App(ctk.CTk):

    # window dimensions
    X = 800
    Y = 440

    def __init__(self):

        super().__init__()

        # setup window
        self.title("metamate")
        self.icon = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), "icons8-m-96.png"))
        self.iconphoto(False, self.icon)
        self.geometry(f"{self.X}x{self.Y}")
        self.minsize(self.X, self.Y)
        self.maxsize(self.X, self.Y)

        # create 10x2 grid system
        self.grid_rowconfigure([r for r in range(10)], weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # CTk variables
        self.variablePth = ctk.StringVar(self)
        self.variableTag = ctk.StringVar(self)
        self.variableSep = ctk.StringVar(self)

        # entry path
        self.path = ctk.CTkEntry(
            self, width=600, height=40, corner_radius=20, textvariable=self.variablePth)
        self.path.insert(0, rootDir)
        self.path.grid(row=2, column=0, columnspan=2, padx=50)

        # button browse
        self.browse = ctk.CTkButton(
            self, text="Browse", width= 600, height=40, corner_radius=20, command=self.chooseDirectory)
        self.browse.grid(row=3, column=0, columnspan=2, padx=50)

        # option-menu tag
        self.tag = ctk.CTkOptionMenu(
            self, width=280, height=40, button_hover_color=("#8593d6", "#171926"), corner_radius=20, variable=self.variableTag, values=list(optionsTag.keys()))
        self.tag.set(list(optionsTag)[0])
        self.tag.grid(row=4, column=0, padx=20, sticky="e")

        # option-menu seperator
        self.sep = ctk.CTkOptionMenu(
            self, width=280, height=40, button_hover_color=("#8593d6", "#171926"), corner_radius=20, variable=self.variableSep, values=list(optionsSep.keys()))
        self.sep.set(list(optionsSep)[0])
        self.sep.grid(row=4, column=1, padx=20, sticky="w")

        # button confirm
        self.confirm = ctk.CTkButton(
            self, text="Go", width=140, height=40, corner_radius=20, command=self.renameFilesInDirectory)
        self.confirm.grid(row=6, columnspan=2)

    # open explorer and set path entry
    def chooseDirectory(self):
        pth = filedialog.askdirectory()
        if pth:
            self.path.delete(0, ctk.END)
            self.path.insert(0, pth)
    
    # generate information and call renaming
    def renameFilesInDirectory(self):
        pth = self.variablePth.get().strip()
        # check that the directory is not the root directory
        if pth != rootDir:
            self.renameFiles(files=glob(os.path.join(pth, "*")), tag=optionsTag[self.variableTag.get()], sep=optionsSep[self.variableSep.get()])
        else:
            print("Warning")    # maintenance
            pass # TODO: warning-icon

    # return whether the file is not hidden
    def notHidden(self, file):
        return not bool(os.stat(file).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

    # discard critical files
    def cleanFiles(self, files):
        # discard subdirectories
        files = filter(os.path.isfile, files)
        # discard hidden files for safety purpose on Windows (glob already ignores file names that start with a dot on Unix)
        if platform.system() == "Windows":
            files = filter(self.notHidden, files)
        return files

    # rename files based on their meta data
    def renameFiles(self, files: list, tag: Tag, sep: Sep):
        # check wheter there are any files to be renamed
        if files:
            # discard critical files
            files = self.cleanFiles(files)
            # list of renamed files
            #renamedFiles = []
            completed = True
            
            for file in files:

                old = os.path.realpath(file)
                root, ext = os.path.splitext(old)
                meta = os.stat(file)

                if(tag == tag.SIZE):
                    appendix = f"{meta[tag.value]}Byte"
                elif(tag in (tag.ACCESS, tag.MODIFICATION, tag.CREATION)):
                    time = localtime(meta[tag.value])
                    appendix = strftime("%Y-%m-%d", time)
                else:
                    print("No tag defined")
                    return

                # build new filename
                new = f"{root}{sep.value}{appendix}{ext}"
                # check that the file was not already renamed
                if appendix not in old:
                    try:
                        # rename from old to new
                        #os.rename(old, new)
                        #renamedFiles.append([old, new])
                        print(f"{old}\n{new}\n{'_' * 100}") # maintenance
                    except:
                        completed = False

            # all files have been renamed
            if completed:
                print("Successful") # maintenance
                pass # TODO: successful-icon
            # not all files have been renamed
            else:
                print("Error")  # maintenance
                pass # TODO: error-icon

        # there are no files to be renamed
        else:
            print("Warning")    #maintenance
            pass # TODO: warning-icon
        # TODO: add renamedFiles[] to logfile


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
