import tkinter as tk  # Primary GUI Library
from tkinter import messagebox
from tkinter import ttk
import os  # Used to check if the csv file is present
import re
import csv  # used to read and write from the csv file


class myApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Test App")
        self.config(bg="skyblue")
        self.data = csvHandler()
        self.data.read()


        self.button_frame = tk.Frame(self, bg="skyblue")
        self.button_frame.pack(fill= tk.BOTH)

        self.add_button = tk.Button(self.button_frame, text="Add Row", command=self.donothing)
        self.add_button.pack(padx=10, pady=10, side="left")

        self.delete_button = tk.Button(self.button_frame, text="Delete Row", command=self.donothing)
        self.delete_button.pack(padx=10, pady=10, side="left")

        self.save_button = tk.Button(self.button_frame, text="Save Changes and exit", command=self.donothing)
        self.save_button.pack(padx=10, pady=10, side="left")

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill= tk.BOTH, expand= True)

        self.tree = None
    def donothing(self):
        print("test")

class editorScreen(tk.Toplevel):
    pass


class csvHandler():
    def __init__(self):
        self.data = []
        self.headers = []
        self.filepath = "allocation.csv"
        pass

    def read(self):
        if not os.path.isfile(self.filepath):
            print("error")
            messagebox.showinfo(message=f"Error: File '{self.filepath}' does not exist.")
            return
        try:
            with open(self.filepath, newline='') as infile:
                reader = csv.reader(infile)
                self.headers = next(reader)
                self.data = list(reader)
        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' not found.")
        except csv.Error as e:
            print(f"Error: Could not read CSV file. {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def write(self):
        with open(self.filepath, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(self.headers)
            writer.writerows(self.data)
        pass

    def add_row(self, to_add):
        self.data.append(to_add)

    def get(self):
        return self.data


if __name__ == "__main__":
    app = myApp()
    app.mainloop()
