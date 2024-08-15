from unittest.mock import patch

from projectTracker import csvHandler

def setup():
    csv_test = csvHandler()
    return csv_test

@patch('tkinter.messagebox.showerror')
def test_name_checks(mock_errorbox):
    csv_test = setup()
    assert 5 == 5
    assert csv_test.value_check("James", "name")==True

    assert csv_test.value_check("68476", "name")==False
    mock_errorbox.assert_called_with(title="Pattern Error", message="The Name should contain only Letters, hyphens, apostrophes")