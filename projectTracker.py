import tkinter as tk  # Primary GUI Library
from tkinter import messagebox
from tkinter import ttk
import os  # Used to check if the csv file is present
import re # used for format validation
import csv  # used to read and write from the csv file


class ResourceManager(tk.Tk):
    '''Resource Manager is a class that contains the main landing screen for this application, It displays the csv data in a clear format, '''
    def __init__(self):
        super().__init__()
        self.geometry("800x350")
        self.title("Resource Allocator")
        self.config(bg="skyblue")
        self.data = csvHandler()
        self.data.read()


        self.button_frame = tk.Frame(self, bg="skyblue")
        self.button_frame.pack(fill= tk.BOTH)

        self.add_button = tk.Button(self.button_frame, text="Add Row", command=self.add_row, bg="lightgreen")
        self.add_button.pack(padx=10, pady=10, side="left")

        self.delete_button = tk.Button(self.button_frame, text="Delete Row", command=self.delete_row, bg="tomato")
        self.delete_button.pack(padx=10, pady=10, side="left")

        self.save_button = tk.Button(self.button_frame, text="Save Changes and exit", command=self.save_exit, bg="snow")
        self.save_button.pack(padx=10, pady=10, side="right")

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill= tk.BOTH, expand= True)

        self.tree=self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.explain_label = tk.Label(text="To edit a value double click on its cell", bg="skyblue")
        self.explain_label.pack(pady=10)

        self.fill_table()
    def save_exit(self):
        self.data.write()
        quit()
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
        row = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        column_index = int(col.replace("#", "")) - 1
        column_name = self.tree["columns"][column_index]
        old_value = self.tree.item(row, "values")[column_index]
        editorScreen(self, row, column_index, column_name, old_value)

    def delete_row(self):
        if self.tree.selection():
            row = self.tree.selection()[0]
            row_index = self.tree.index(row)
            self.data.delete(row_index)
            self.fill_table()
        else:
            messagebox.showwarning(title="Error", message="Select a row first")
    def add_row(self):
        addScreen(self)

class editorScreen(tk.Toplevel):
    def __init__(self, parent, row, col, col_name, old_value):
        super().__init__(parent)
        self.title("Edit Value")
        self.geometry("300x200")
        self.config(bg="skyblue")
        self.parent = parent
        self.row = row
        self.col = col
        self.col_name = col_name

        self.edit_label = (tk.Label(self, text="Edit value:", bg="skyblue"))
        self.edit_label.pack(pady=10)
        self.new_value_input = tk.Entry(self)
        self.new_value_input.pack(pady=10)
        self.new_value_input.insert(0, old_value)

        self.save_button = tk.Button(self, text="Save", command=self.save_edit, bg="lightgreen")
        self.save_button.pack(pady=10)
    def save_edit(self):
        new_value = self.new_value_input.get()
        if self.parent.data.value_check(new_value, self.col_name):
            self.parent.tree.set(self.row, column=self.parent.tree["columns"][self.col], value=new_value)
            self.parent.data.update(self.parent.tree)
        self.destroy()


class addScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Row")
        self.geometry("300x400")
        self.config(bg="skyblue")
        self.parent = parent

        self.name_label = tk.Label(self, text="Name:", bg="skyblue")
        self.name_input = tk.Entry(self)
        self.name_label.pack()
        self.name_input.pack(pady=10)

        self.project_label = tk.Label(self, text="Project:", bg="skyblue")
        self.project_input = tk.Entry(self)
        self.project_label.pack()
        self.project_input.pack(pady=10)

        self.role_label = tk.Label(self, text="Role:", bg="skyblue")
        self.role_input = tk.Entry(self)
        self.role_label.pack()
        self.role_input.pack(pady=10)

        self.time_label = tk.Label(self, text="Percentage of Time Allocated:", bg="skyblue")
        self.time_input = tk.Entry(self)
        self.time_label.pack()
        self.time_input.pack(pady=10)

        self.save_button = tk.Button(self, text="Save", command=self.save_edit, bg="lightgreen")
        self.save_button.pack(pady=10)
    def save_edit(self):
        if self.parent.data.value_check(self.name_input.get(), "name"):
            if self.parent.data.value_check(self.project_input.get(), "project"):
                if self.parent.data.value_check(self.name_input.get(), "name"):
                    if self.parent.data.value_check(self.time_input.get(), "time allocated"):
                        self.parent.data.add([self.name_input.get(),self.project_input.get(),self.role_input.get(),self.time_input.get()])
                        self.parent.fill_table()

        self.destroy()


class csvHandler():
    def __init__(self):
        self.data = []
        self.headers = []
        self.filepath = "allocations.csv"
        pass
    def normalize(self, value):
        return value.strip().lower()
    def value_check(self, value, type):
        type_normalized = self.normalize(type)
        try:
            match (type_normalized):
                case "name":
                    if self.precence_check(self.normalize(value)):
                        if self.length_check(value):
                            if self.name_format_check(self.normalize(value)):
                                return True
                            else:
                                messagebox.showerror(title="Pattern Error",
                                                     message="The Name should contain only Letters, hyphens, apostrophes")
                        else:
                            messagebox.showerror(title="Length Error",
                                                 message="Name should be between 3 and 35 characters long")
                    else:
                        messagebox.showerror(title="Presence Error",
                                             message="Please Enter a Value for the name")
                    return False
                case "project":
                    if self.precence_check(self.normalize(value)):
                        if self.length_check(value):
                            if self.name_format_check(self.normalize(value)):
                                return True
                            else:
                                messagebox.showerror(title="Pattern Error",
                                                     message="The Name should contain only Letters, hyphens, apostrophes")
                        else:
                            messagebox.showerror(title="Length Error",
                                                 message="Project Name should be between 3 and 35 characters long")
                    else:
                        messagebox.showerror(title="Presence Error",
                                             message="Please Enter a Value for the project name")
                    return False
                case "role":
                    if self.precence_check(self.normalize(value)):
                        if self.length_check(value):
                            if self.name_format_check(self.normalize(value)):
                                return True
                            else:
                                messagebox.showerror(title="Pattern Error",
                                                     message="The Name should contain only Letters, hyphens, apostrophes")
                        else:
                            messagebox.showerror(title="Length Error",
                                                 message="Role Title should be between 3 and 35 characters long")
                    else:
                        messagebox.showerror(title="Presence Error", message="Please Enter a Value for the role title")
                    return False
                case "time allocated":
                    if self.precence_check(value.strip()):
                        if self.percentage_check(value):
                            return True
                        else:
                            messagebox.showerror(title="Pattern Error",
                                                 message="Value should be an interger between 1 - 80")
                    else:
                        messagebox.showerror(title="Presence Error",
                                             message="Please Enter a Value for the Time Allocated")
                case _:
                    messagebox.showerror(title="Error", message="Value type unknown, Checks fail")
                    return False
        except Exception as e:
            messagebox.showerror(title="Error",
                                 message=f"An Unknown error has occured: {e}")
            return False
    def precence_check(self, value):
        if value:
            return True
        return False
    def length_check(self, value):
        return 2<len(value)<=35
    def name_format_check(self, value):
        pattern = re.compile(r"^[A-Za-z '-]+$")
        return  bool(pattern.match(value))
    def percentage_check(self, value):
        pattern = re.compile(r"\b(80|[1-7]?[0-9])\b|\b(80|[1-7]?[0-9]%)\b")
        return bool(pattern.match(value))
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
        except Exception as e:
            messagebox.showerror(f"An unexpected error occurred: {e}")

    def write(self):
        with open(self.filepath, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(self.headers)
            writer.writerows(self.data)
        pass

    def add(self, to_add):
        self.data.append(to_add)

    def delete(self, index):
        self.data.pop(index)

    def update(self, tree):
        self.data=[]
        for item in tree.get_children():
            values = tree.item(item)["values"]
            self.data.append(values)
    def get(self):
        return self.data


if __name__ == "__main__":
    app = ResourceManager()
    app.mainloop()
