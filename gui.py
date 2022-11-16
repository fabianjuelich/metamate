import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# setting appearance and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):

    x = 800
    y = 440

    def __init__(self):

        super().__init__()

        # configure window
        self.title("metamate")
        self.minsize(self.x, self.y)
        self.maxsize(self.x, self.y)
        self.geometry(f"{self.x}x{self.y}")

        # create 10x2 grid system
        self.grid_rowconfigure([e for e in range(10)], weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # path entry
        self.path = ctk.CTkEntry(
            placeholder_text="/", width=600, height=40, corner_radius=20)

        self.path.grid(row=2, column=0, columnspan=2, padx=50)

        # browse button
        self.browse = ctk.CTkButton(
            text="Browse", width= 600, height=40, corner_radius=20, command=directory)

        self.browse.grid(row=3, column=0, columnspan=2, padx=50)

        # tag option menu
        self.tag = ctk.CTkOptionMenu(
            width=280, height=40, button_color="#11B384", button_hover_color="#0D8A66", values=["Creation Date", "Modification Date", "Access Date", "Size"], corner_radius=20)

        self.tag.set("Creation Date")

        self.tag.grid(row=4, column=0, padx=20, sticky="e")

        # seperator option menu
        self.sep = ctk.CTkOptionMenu(
            width=280, height=40, button_color="#11B384", button_hover_color="#0D8A66", values=["_", "-", ".", " "], corner_radius=20)

        self.sep.set("_")

        self.sep.grid(row=4, column=1, padx=20, sticky="w")

        # ok button
        self.ok = ctk.CTkButton(
            text="Go", width=140, height=40, corner_radius=20)

        self.ok.grid(row=6, columnspan=2)


# open explorer
def directory():
    filedialog.askdirectory()


if __name__ == "__main__":
    app = App()
    app.mainloop()
