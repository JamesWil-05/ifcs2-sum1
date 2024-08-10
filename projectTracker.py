import tkinter as tk  # Primary GUI Library
from tkinter import messagebox
from tkinter import ttk
import os  # Used to check if the csv file is present
import re
import csv  # used to read and write from the csv file


class ResourceManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x200")
        self.title("Resource Allocator")
        self.config(bg="skyblue")
        self.data = csvHandler()
        self.data.read()


        self.button_frame = tk.Frame(self, bg="skyblue")
        self.button_frame.pack(fill= tk.BOTH)

        self.add_button = tk.Button(self.button_frame, text="Add Row", command=self.donothing, bg="lightgreen")
        self.add_button.pack(padx=10, pady=10, side="left")

        self.delete_button = tk.Button(self.button_frame, text="Delete Row", command=self.donothing, bg="tomato")
        self.delete_button.pack(padx=10, pady=10, side="left")

        self.save_button = tk.Button(self.button_frame, text="Save Changes and exit", command=quit, bg="snow")
        self.save_button.pack(padx=10, pady=10, side="right")

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill= tk.BOTH, expand= True)
        self.tree= None
        self.fill_table()
    def donothing(self):
        print("test")
    def fill_table(self):
        if self.tree:
            self.tree.destroy()
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.config(columns= self.data.headers,
                         show = "headings")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        for row in self.data.data:
            self.tree.insert("", "end", values=row)

        self.tree.bind("<Double-1>", self.edit_val)
    def edit_val(self, event):
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        column_index = int(col.replace("#", "")) - 1
        column_name = self.tree["columns"][column_index]
        old_value = self.tree.item(item, "values")[column_index]


        editorScreen(self, item, column_index, column_name, old_value)
class editorScreen(tk.Toplevel):
    def __init__(self, parent, item, col_index, col_name, old_value):
        super().__init__(parent)
        self.title("Edit Value")
        self.geometry("300x200")
        self.parent = parent
        self.item = item
        self.col_index = col_index

        tk.Label(self, text="Edit value:").pack(pady=10)
        self.new_value_entry = tk.Entry(self)
        self.new_value_entry.pack(pady=10)
        self.new_value_entry.insert(0, old_value)

        tk.Button(self, text="Save", command=self.save_edit).pack(pady=10)
    def save_edit(self):
        self.destroy()




class csvHandler():
    def __init__(self):
        self.data = []
        self.headers = []
        self.filepath = "allocations.csv"
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
            messagebox.showerror(f"Error: File '{self.filepath}' not found.")
        except csv.Error as e:
            messagebox.showerror(f"Error: Could not read CSV file. {e}")
        except Exception as e:
            messagebox.showerror(f"An unexpected error occurred: {e}")

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
    app = ResourceManager()
    app.mainloop()
