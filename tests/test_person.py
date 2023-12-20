from pprint import pprint

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from requests import Response

from src.person import Person


# Fixture to create a Person instance
@pytest.fixture
def john_doe_person():
    return Person(name="John Doe", age=30, ssn="123-45-6789")


# Fixture to create a Person instance with a phone number
@pytest.fixture
def jane_smith_person():
    person = Person(name="Jane Smith", age=25, ssn="987-65-4321")
    person.phones.append("555-1234")
    return person


# Fixture to create a Person instance with an email address
@pytest.fixture
def alice_johnson_person():
    person = Person(name="Alice Johnson", age=35, ssn="543-21-8765")
    person.emails.append("alice@example.com")
    return person


# Fixture to create a Person instance with a profession
@pytest.fixture
def bob_brown_person():
    person = Person(name="Bob Brown", age=40, ssn="876-54-3210")
    person.professions.append("Software Engineer")
    return person


@pytest.fixture
def mock_requests_get_200(mocker) -> Response:
    def _mock_requests_get_200(url):
        mock_response: Response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200

        # Define the JSON data you want to simulate
        json_data = [
            {"name": "John Doe", "age": 30, "ssn": "123-45-6789"},
            {"name": "Jane Smith", "age": 25, "ssn": "987-65-4321"},
            {"name": "Alice Johnson", "age": 35, "ssn": "543-21-8765"}
        ]

        # Mock the json method to return the predefined data
        mock_response.json.return_value = json_data

        return mock_response

    return _mock_requests_get_200


@pytest.fixture
def mock_requests_get_404(mocker):
    def _mock_requests_get_404(url):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 404  # Simulate a 404 error

        return mock_response

    return _mock_requests_get_404


# Test cases using fixtures
def test_person_attributes(john_doe_person):
    # Assert
    assert john_doe_person.name == "John Doe"
    assert john_doe_person.age == 30
    assert john_doe_person.ssn == "123-45-6789"
    assert john_doe_person.phones == []
    assert john_doe_person.emails == []
    assert john_doe_person.professions == []


def test_add_phone(jane_smith_person):
    # Act
    jane_smith_person.phones.append("555-5678")

    # Assert
    assert jane_smith_person.phones == ["555-1234", "555-5678"]


def test_add_email(alice_johnson_person):
    # Act
    alice_johnson_person.emails.append("alice.j@example.com")

    # Assert
    assert alice_johnson_person.emails == ["alice@example.com", "alice.j@example.com"]


def test_add_profession(bob_brown_person):
    # Act
    bob_brown_person.professions.append("Data Scientist")

    # Assert
    assert bob_brown_person.professions == ["Software Engineer", "Data Scientist"]


def test_john_deo_age(john_doe_person):
    john_doe_person.age = "thirty"
    # print(john_doe_person)


# Test case assert exception
def test_age_division_zero(john_doe_person):
    # 20 / 0 --> ZeroDivisionError with msg="division by zero"
    # Act and Assert
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        john_doe_person.age = 20 / 0


def test_get_persons_from_api_200(mock_requests_get_200: Response, monkeypatch: MonkeyPatch):
    # Arrange
    monkeypatch.setattr("requests.get", mock_requests_get_200)

    # Act
    api_url = "https://example.com/api/persons"
    persons_list = Person.get_persons_from_api(api_url)

    # assert
    # pprint(persons_list)
    assert len(persons_list) == 3
    assert isinstance(persons_list[0], Person)
    assert persons_list[0].name == "John Doe"
    assert persons_list[1].name == "Jane Smith"
    assert persons_list[2].name == "Alice Johnson"


# Test case for get_persons_from_api with mocked request returning 404
def test_get_persons_from_api_404(mock_requests_get_404, monkeypatch: MonkeyPatch):
    # Arrange
    api_url = "https://example.com/api/persons"
    monkeypatch.setattr('requests.get', mock_requests_get_404)

    # Act & asser
    api_url = "https://example.com/api/persons"
    with pytest.raises(Exception, match="Http Error, status_code: 404"):
        Person.get_persons_from_api(api_url)
