from unittest.mock import MagicMock


class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def get_data():
        return 'Original Data'


def test_magic_mock():
    # Creating a MagicMock object to replace the add method
    mock_calculator = MagicMock(spec=Calculator)

    # Configuring the return value of the add method
    mock_calculator.add.return_value = 10

    # Using the MagicMock in a test
    result = mock_calculator.add(2, 7)

    # Asserting that the add method was called with the correct arguments
    mock_calculator.add.assert_called_once_with(2, 7)

    # Asserting the result
    assert result == 10


def test_patch_get_data(monkeypatch):
    # Original behavior before patching
    assert Calculator.get_data() == "Original Data"

    # Patching the get_data function to return "Patched Data"
    def patched_get_data():
        return "Patched Data"

    monkeypatch.setattr(Calculator, "get_data", patched_get_data)

    # After patching, the behavior of get_data is modified
    assert Calculator.get_data() == "Patched Data"
