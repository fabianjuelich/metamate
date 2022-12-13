"""
Dependencies:
Python 3.9.2
Python3-tk
CustomTkinter 4.6.3 (pip3)
icons8-m-96.png
"""

import sys
import os
import platform
import stat
import logging
from glob import glob
from enum import Enum
from time import strftime, localtime
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import atexit

# root directory for placeholder-text and safety purposes
rootDir = os.path.abspath(os.sep)

# get home directory
home = os.path.expanduser("~")

# change current working directory to script path
try:
    os.chdir(os.path.dirname(__file__))
except:
    # abort
    sys.exit("cwd can not be changed")

# constants
class Tag(Enum):
    CREATION = 9    # TODO: wrongdoing: changed to current date after renaming file on linux
    MODIFICATION = 8
    ACCESS = 7
    SIZE = 6

class Sep(Enum):
    UNDERSCORE = "_"
    DASH = "-"
    DOT = "."
    SPACE = " "

# configure and create logger
logFormat = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    filename=("metamate.log"),
    level=logging.INFO,
    format=logFormat)
logger = logging.getLogger()

class App(ctk.CTk):

    # appearance and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("sweetkind")

    # window dimensions
    X = 800
    Y = 440

    # options for renaming
    optionsTag = dict(zip(["Creation Date", "Modification Date", "Access Date", "Size"], list(Tag)))
    optionsSep = dict(zip(["_", "-", ".", " "], list(Sep)))

    def __init__(self):

        super().__init__()

        # setup window
        self.title("metamate")
        self.icon = tk.PhotoImage(file = "icons8-m-96.png")
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
        self.path.grid(row=3, column=0, columnspan=2, padx=50)

        # button browse
        self.browse = ctk.CTkButton(
            self, text="Browse", width= 600, height=40, corner_radius=20, command=self.chooseDirectory)
        self.browse.grid(row=4, column=0, columnspan=2, padx=50)

        # option-menu tag
        self.tag = ctk.CTkOptionMenu(
            self, width=280, height=40, button_hover_color=("#8593d6", "#171926"), corner_radius=20, variable=self.variableTag, values=list(self.optionsTag.keys()))
        self.tag.set(list(self.optionsTag)[0])
        self.tag.grid(row=5, column=0, padx=20, sticky="e")

        # option-menu seperator
        self.sep = ctk.CTkOptionMenu(
            self, width=280, height=40, button_hover_color=("#8593d6", "#171926"), corner_radius=20, variable=self.variableSep, values=list(self.optionsSep.keys()))
        self.sep.set(list(self.optionsSep)[0])
        self.sep.grid(row=5, column=1, padx=20, sticky="w")

        # button confirm
        self.confirm = ctk.CTkButton(
            self, text="Go", width=140, height=40, corner_radius=20, command=self.renameFilesInDirectory)
        self.confirm.grid(row=7, columnspan=2)

        # label message
        self.message = ctk.CTkLabel(
            self, text="", width=200, height=40, corner_radius=20)
        self.message.grid(row = 8, columnspan=2)

    # set message in label
    def setMessage(self, msg:str):
        self.message.configure(text=msg)

    # clear message in label
    def clearMessage(self):
        self.setMessage("")

    # open explorer and set path entry
    def chooseDirectory(self):
        pth = filedialog.askdirectory(initialdir=home)
        if pth:
            self.path.delete(0, ctk.END)
            self.path.insert(0, pth)
    
    # generate information and call renaming
    def renameFilesInDirectory(self):
        logger.info("Execute")
        pth = self.variablePth.get().strip()
        # check that the directory exists
        if not os.path.isdir(pth):
            logger.warning(f"Non-existent directory: '{pth}'")
            self.setMessage("Non-existent directory")   # TODO: warning-icon
        # check that the directory is not the root directory
        elif pth == rootDir:
            logger.warning(f"Files in root directory cannot be renamed: '{pth}'")
            self.setMessage("Choose valid directory")   # TODO: warning-icon
        # rename
        else:
            self.renameFiles(files=glob(os.path.join(pth, "*")), tag=self.optionsTag[self.variableTag.get()], sep=self.optionsSep[self.variableSep.get()])
        logger.info("Finish")

    # return whether the file is not hidden
    def notHidden(self, file):
        return not bool(os.stat(file).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

    # discard critical files
    def cleanFiles(self, files):
        # check that file exists and discard subdirectories
        files = filter(os.path.isfile, files)
        # discard hidden files for safety purpose on Windows (glob already ignores file names that start with a dot on Unix)
        if platform.system() == "Windows":
            files = filter(self.notHidden, files)
        return list(files)

    # rename files based on their meta data, handle exceptions and write to logfile
    def renameFiles(self, files: list, tag: Tag, sep: Sep):
        # discard critical files
        files = self.cleanFiles(files)
        # abort if there are no files to rename
        if not files:
            logger.warning("No files to rename")    # TODO: log directory
            self.setMessage("Directory is empty")   # TODO: warning-icon
            return

        # for analyzing
        some = False
        complete = True
        already = False
        failure = False
        
        for file in files:

            # collect and generate information
            old = os.path.realpath(file)
            root, ext = os.path.splitext(old)
            meta = os.stat(file)

            if(tag == tag.SIZE):
                appendix = f"{meta[tag.value]}Byte"
            elif(tag in (tag.ACCESS, tag.MODIFICATION, tag.CREATION)):
                time = localtime(meta[tag.value])
                appendix = strftime("%Y-%m-%d", time)
            else:
                logger.error("Tag not defined")
                return

            # build new filename
            new = f"{root}{sep.value}{appendix}{ext}"

            # check that the file is not named that way yet
            if appendix in old:
                already = True
                complete = False
                logger.warning(f"'{old}' has already been named that way '{appendix}'")
            else:
                try:
                    # rename from old to new
                    os.rename(old, new)
                    some = True
                    logger.info(f"'{old}' renamed to '{new}'")
                except:
                    failure = True
                    complete = False
                    logger.error(f"'{old}' could not be renamed to '{new}'")

        # conclusion    # TODO: feedback-icons
        if some and complete:
            logger.info("Success: all files have been renamed")
            self.setMessage("Succesful")
        elif some and already and not failure:
            logger.warning("Success: some files were already named that way")
            self.setMessage("Successful (some files were already named correctly)")
        elif some and failure and not already:
            logger.error("Succes: some files could not have been renamed")
            self.setMessage("Successful (but something went wrong)")
        elif some and failure and already:
            logger.error("Success: something went wrong and some files were already named that way")
            self.setMessage("Successful (but something went wrong and some files were already named correctly)")
        elif already and failure:
            logger.error("Fail: something went wrong and some files were already named that way")
            self.setMessage("Failure (something went wrong and some files were already named correctly)")
        elif already:
            logger.error("Success: all files are already named that way")
            self.setMessage("Successful (all files were already named correctly)")
        elif failure:
            logger.error("Fail: no files have been renamed")
            self.setMessage("Failure (something went wrong)")
        else:
            logger.error("Fail")
            self.setMessage("Failure")


def exitHandler():
    logger.info("Exit")

def main():
    logger.info("Startup")
    app = App()
    app.mainloop()
    atexit.register(exitHandler)

if __name__ == "__main__":
    main()
    # log exit
