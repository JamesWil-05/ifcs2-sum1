import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
import csv

class myApp(tk.Tk):
    def __init__(self):
            super().__init__()
            self.geometry("500x400")
            self.title("Test App")
            self.config(bg = "skyblue")


class editorScreen(tk.Frame):
     pass
class csvHandler():
     pass

if __name__=="__main__":
    app= myApp()
    app.mainloop()
