from unittest.mock import patch, mock_open

from projectTracker import csvHandler

def setup():
    csv_test = csvHandler()
    return csv_test

def test_value_checks_valid():
    csv_test = setup()

    assert csv_test.value_check("John Doe", "name") == True

    assert csv_test.value_check("AR Glasses", "project") == True

    assert csv_test.value_check("Developer", "role") == True

    assert csv_test.value_check("50", "time allocated") == True

    assert csv_test.value_check("50%", "time allocated") == True


'''The same checks are preformed on Name, Project Title and Role Title, so each test function will test for errors with different parameters'''
@patch('tkinter.messagebox.showerror')
def test_value_checks_invalid_name (mock_errorbox):
    csv_test = setup()
    assert csv_test.value_check("68476", "name")==False
    mock_errorbox.assert_called_with(title="Pattern Error", message="The Name should contain only Letters, hyphens, apostrophes")

    assert csv_test.value_check("me", "name")==False
    mock_errorbox.assert_called_with(title="Length Error", message="Name should be between 3 and 35 characters long")

    assert csv_test.value_check(" ", "name") == False
    mock_errorbox.assert_called_with(title="Presence Error", message="Please Enter a Value for the name")

@patch('tkinter.messagebox.showerror')
def test_value_checks_invalid_project (mock_errorbox):
    csv_test = setup()
    assert csv_test.value_check("500.83", "project")==False
    mock_errorbox.assert_called_with(title="Pattern Error", message="The Name should contain only Letters, hyphens, apostrophes")

    assert csv_test.value_check("ag", "project")==False
    mock_errorbox.assert_called_with(title="Length Error", message="Project Name should be between 3 and 35 characters long")

    assert csv_test.value_check("", "project") == False
    mock_errorbox.assert_called_with(title="Presence Error", message="Please Enter a Value for the project name")

@patch('tkinter.messagebox.showerror')
def test_value_checks_invalid_role (mock_errorbox):
    csv_test = setup()
    assert csv_test.value_check("000", "role")==False
    mock_errorbox.assert_called_with(title="Pattern Error", message="The Name should contain only Letters, hyphens, apostrophes")

    assert csv_test.value_check("50", "role")==False
    mock_errorbox.assert_called_with(title="Length Error", message="Role Title should be between 3 and 35 characters long")

    assert csv_test.value_check(" ", "role") == False #non-breaking space character ctrl shift U 00a0
    mock_errorbox.assert_called_with(title="Presence Error", message="Please Enter a Value for the role title")

@patch('tkinter.messagebox.showerror')
def test_value_checks_invalid_time (mock_errorbox):
    csv_test = setup()
    assert csv_test.value_check("500.83", "time allocated")==False
    mock_errorbox.assert_called_with(title="Pattern Error", message="Value should be an integer between 1 - 80")

    assert csv_test.value_check("-70", "time allocated")==False
    mock_errorbox.assert_called_with(title="Pattern Error", message="Value should be an integer between 1 - 80")

    assert csv_test.value_check(" ", "name") == False
    mock_errorbox.assert_called_with(title="Presence Error", message="Please Enter a Value for the name")

@patch('tkinter.messagebox.showerror')
def test_value_checks_edge_cases (mock_errorbox):
    csv_test = setup()
    assert csv_test.value_check("1", "time allocated")==True

    assert csv_test.value_check("0", "time allocated") == False
    mock_errorbox.assert_called_with(title="Pattern Error", message="Value should be an integer between 1 - 80")

    assert csv_test.value_check("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "name") == False
    mock_errorbox.assert_called_with(title="Length Error", message="Name should be between 3 and 35 characters long")

def test_data_read():
    csv_test = setup()

    csv_test.read()
    assert csv_test.get() == [['John Smith', ' VR Training', ' Project Manager', ' 50'], ['Jane Doe', ' Chatbot', ' Developer', ' 30'], ['Katie Phillips', ' Automation', ' Business Analyst', ' 60']]

def test_data_add():
    csv_test = setup()
    csv_test.add(['Greg Lestrade', 'Search', 'Tester', '40'])

    assert csv_test.get() == [['Greg Lestrade', 'Search', 'Tester', '40']]


def test_data_delete():
    csv_test = setup()
    csv_test.read()
    csv_test.delete(2)
    assert csv_test.get() == [['John Smith', ' VR Training', ' Project Manager', ' 50'], ['Jane Doe', ' Chatbot', ' Developer', ' 30']]

def test_data_normalize():
    csv_test = setup()
    assert csv_test.normalize("Maisy Hudson") == "maisy hudson"
    assert csv_test.normalize("MAISY HUDSON    ") == "maisy hudson"

    assert csv_test.normalize_title("maisy hudson") == "Maisy Hudson"
    assert csv_test.normalize_title("chatbot (proof of concept)") == "Chatbot (Proof Of Concept)"

    assert csv_test.normalize("50 %") == "50 %"


