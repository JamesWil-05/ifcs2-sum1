import tkinter as tk  # Primary GUI Library
from tkinter import messagebox # import the tk message box feature for errors
from tkinter import ttk # import ttk package for treeview widget
import os  # Used to check if the csv file is present
import re # used for format validation
import csv  # used to read and write from the csv file


class ResourceManager(tk.Tk):
    '''Resource Manager is a class that contains the main landing screen for this application, It contains the configs for the window itself,
    as well as the widgets in use on the main screen.
    The Purpose of the window is to display the data loaded from the csv in the treeview widget self.tree.
    The data is loaded into this window using the csv Handeler Object'''
    def __init__(self):
        super().__init__()
        self.geometry("800x350")
        self.title("Resource Allocator")
        self.config(bg="skyblue")
        self.data = csvHandler()
        self.data.read()


        self.button_frame = tk.Frame(self, bg="skyblue") #Button Frame is used to display the control buttons side by side, all over the tree frame
        self.button_frame.pack(fill= tk.BOTH) # Packs the Frame, ensuring it expands into the available space

        #Instantiate and pack each button
        self.add_button = tk.Button(self.button_frame, text="Add Row", command=self.add_row, bg="lightgreen")
        self.add_button.pack(padx=10, pady=10, side="left")

        self.delete_button = tk.Button(self.button_frame, text="Delete Row", command=self.delete_row, bg="tomato")
        self.delete_button.pack(padx=10, pady=10, side="left")

        self.save_button = tk.Button(self.button_frame, text="Save Changes and exit", command=self.save_exit, bg="snow")
        self.save_button.pack(padx=10, pady=10, side="right")

        #Instansiate and pack the tree frame, used to contain the data table
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill= tk.BOTH, expand= True)

        self.tree=self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.explain_label = tk.Label(text="To edit a value double click on its cell", bg="skyblue")
        self.explain_label.pack(pady=10)

        self.fill_table()
    def save_exit(self): # This triggers when self.save_button is triggered, it saves the new data to the csv file, then quits the program
        self.data.write()
        quit()
    def fill_table(self):
        '''Method for Filling the treeview with up to date data.
         '''
        if self.tree: # Removes previous table, to replace with new data
            self.tree.destroy()
        self.tree = ttk.Treeview(self.tree_frame)  #Instansiates the new treeview object, setting the frame to tree_frame
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.config(columns= self.data.headers, #Names columns using headers from the data object
                         show = "headings")

        for col in self.tree["columns"]: # Sets each heading equal to the repective column name
            self.tree.heading(col, text=col)
        for row in self.data.data: # Inserts data into table
            self.tree.insert("", "end", values=row)

        self.tree.bind("<Double-1>", self.edit_val) # Enables action to update a value using double left click
    def edit_val(self, click): # A Method used to collect information for the editor screen, used for changing a value
        row = self.tree.selection()[0] # Gets row id
        col = self.tree.identify_column(click.x) # gets column id
        column_index = int(col.replace("#", "")) - 1 # converts column id into index format for csv handler
        column_name = self.tree["columns"][column_index] # gets name of column for error checking
        old_value = self.tree.item(row, "values")[column_index] # gets current value, to autofill the textbox in the new window with it
        editorScreen(self, row, column_index, column_name, old_value) # instantiates the editor screen, setting main window as parent

    def delete_row(self): # A method used to remove a row from the data set
        if self.tree.selection(): # checks the the user has selected a row to delete
            row = self.tree.selection()[0]# gets the first row selected (in case multiple were selected)
            row_index = self.tree.index(row)
            self.data.delete(row_index)# deletes the row from the main data set using row index
            self.fill_table() # updates table to reflect change
        else: # if not cancel operation with error popup
            messagebox.showwarning(title="Error", message="Select a row first")
    def add_row(self): # method to open add row screen
        addScreen(self)

class editorScreen(tk.Toplevel):
    '''This class is used to create an editor screen to edit a specific cell. it uses previously collected data about the selected value to preform error checks
    on the new proposed value.'''
    def __init__(self, parent, row, col, col_name, old_value): # initialise the new window
        super().__init__(parent)
        self.title(f"Edit {col_name}")
        self.geometry("300x200")
        self.config(bg="skyblue")
        self.parent = parent # sets parent of window to be main window
        self.row = row
        self.col = col
        self.col_name = col_name

        self.edit_label = (tk.Label(self, text=f"Edit {col_name}:", bg="skyblue")) # A Label explaining what this window is for
        self.edit_label.pack(pady=10)

        self.new_value_input = tk.Entry(self) # the input box for the new value to be inserted
        self.new_value_input.pack(pady=10)
        self.new_value_input.insert(0, old_value) # sets the input field text to the current value, in order the make it clear what the user is changing

        self.save_button = tk.Button(self, text="Save", command=self.save_edit, bg="lightgreen") # Button to trigger checks on the new value, if they pass then the change is applied
        self.save_button.pack(pady=10)
    def save_edit(self):
        new_value = self.new_value_input.get() # gets the new input
        if self.parent.data.value_check(new_value, self.col_name): #runs checks based off the column name ot determine the required checks
            self.parent.tree.set(self.row, column=self.parent.tree["columns"][self.col], value=new_value) #updates tree with new value
            self.parent.data.update(self.parent.tree) #uses tree to update dataset
        self.destroy() # close window once process is finished

class addScreen(tk.Toplevel):
    '''Class for window for adding a new row to the table. This class allows a user to input data for each field,
    runs check on each field, and if they pass, the dataset is appended with the new value'''
    def __init__(self, parent):# initialise the new window
        super().__init__(parent)
        self.title("Add Row")
        self.geometry("300x400")
        self.config(bg="skyblue")
        self.parent = parent

        #Each input box is creates along side a label describing what is required for each input
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

        self.save_button = tk.Button(self, text="Save", command=self.save_edit, bg="lightgreen") # A button to trigger the value checks and saving of the data
        self.save_button.pack(pady=10)
    def save_edit(self):
        if self.parent.data.value_check(self.name_input.get(), "name"): # each value is tested, and is all pass then the data is added
            if self.parent.data.value_check(self.project_input.get(), "project"):
                if self.parent.data.value_check(self.name_input.get(), "name"):
                    if self.parent.data.value_check(self.time_input.get(), "time allocated"):
                        self.parent.data.add([self.name_input.get(),self.project_input.get(),self.role_input.get(),self.time_input.get()]) # adds data to csv handeler
                        self.parent.fill_table() # refreshes the table with new data
        self.destroy() # closes the add row window

class csvHandler():
    '''A class used as a ultility for managing the csv data throughout the program
     This class is used to read and write the data to the csv file as well as hold the data referenced by the treeview widget,
     including fuctions to append, update and delete data from this dataset
     additionally this class is used to check a proposed new value to be added to the csv'''
    def __init__(self):
        self.data = [] # this will hold the referenced data
        self.headers = ["Name", "Project", "Role", "Time Allocated"] # this holds the headers for each column of the table
        self.filepath = "allocations.csv" # this is the file that will be read and written to
    def normalize(self, value): # This normalises a value  (used for both the headers and data types
        return value.strip().lower()
    def value_check(self, value, type):
        '''This Function is used to call other funcions based on the type it is called with, the value then goes through several checks.
        If the value fails any check then a message box is triggered and the function returns false, informing the caller not to make the proposed changes'''
        type_normalized = self.normalize(type)
        try:
            match (type_normalized): # Switch statement for each value heading
                case "name":
                    if self.precence_check(self.normalize(value)):
                        if self.length_check(value):
                            if self.name_format_check(self.normalize(value)):
                                return True # if all checks pass return true
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
        except Exception as e: # incase an unknown error occurs during checks like value error, will return false to caller
            messagebox.showerror(title="Error",
                                 message=f"An Unknown error has occured: {e}")
            return False
    def precence_check(self, value): # checks is there is a value stored in the variable
        if value:
            return True
        return False
    def length_check(self, value):# checks the value length is within justified range
        return 2<len(value)<=35
    def name_format_check(self, value): # checks the name only contains alphabetic characters as well as some punctuation included in names
        pattern = re.compile(r"^[A-Za-z '-]+$")
        return  bool(pattern.match(value))
    def percentage_check(self, value):
        pattern = re.compile(r"\b(80|[1-7]?[0-9])\b|\b(80|[1-7]?[0-9]%)\b") # checks if the number is a number between 0 and 80 as the percent should be between these two. Also checks for and allows the inclusion of a %
        return bool(pattern.match(value))
    def read(self):
        if not os.path.isfile(self.filepath): # checks if file exists
            print("error")
            messagebox.showinfo(message=f"Error: File '{self.filepath}' does not exist.")
            return
        try:
            with open(self.filepath) as infile: # opens file to be read
                reader = csv.reader(infile)
                self.data = list(reader)# converts each line of the file, bar the first, into a list
        except Exception as e:
            messagebox.showerror(f"An unexpected error occurred: {e}")

    def write(self):
        with open(self.filepath, 'w') as outfile: # opens file to overwrite
            writer = csv.writer(outfile)
            writer.writerows(self.data) # writes updated data to file

    def add(self, to_add): # function to add a row to data
        self.data.append(to_add)

    def delete(self, index):
        self.data.pop(index) # removes row at selected index from data

    def update(self, tree): # function for overwriting data with updated version
        self.data=[] # sets current data to none
        for item in tree.get_children(): # gets all rows from table
            values = tree.item(item)["values"]
            self.data.append(values) # inserts rows into table
    def get(self): # simple function to send data to caller
        return self.data

if __name__ == "__main__":
    app = ResourceManager() # instantiates main app
    app.mainloop()