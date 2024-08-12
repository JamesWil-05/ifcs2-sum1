+ Should provide a clear and intuitive interface

+ Should be able to import data from a csv file

+ Should be able to write edited data into the same csv file
+ The program should launch into a tkinter window on application start
+ The Main program window should display a table of the data imported from the csv file
+ The main program window should feature 3 buttons for Adding / Removing a row and saving the changes before closing the program
+ destructive actions (like deletion) should be marked in red to indicate to the user that the item will be removed
+ Creative actions like Adding a row or saving a value change should be marked in green
+ The user should be able to double click any value in the table in order to edit the value 
+ the add and edit row actions should open up a new window with input dialogue dependant on the value being changd 
+ 

The program should prevent errors in various circumstances:    

+ If The user attempts to delete a row without selecting one the program will pop up informing them that they need to select a row first
+ If the user attempts to input Data that is not intended for the value type (such as a string for percentage time allocated) the program will cancel the 'change' operation informing them of the reason the data was invaild.
+ If the program fails to load the csv, either due to incorrect formatting or due to the file being missing, the program will inform the user and the user will be presented with an empty treeview to make changes to.
+ The error messages throughout the program should be informative to the user, and if values need updating to reflect the error then the error should explain the reason the value did not pass the validation checks

---

###### ps user may not be able to add values to the treeview without the csv present due to header issues.