import http
from dataclasses import dataclass, field
from typing import List
import requests


@dataclass
class Person:
    name: str
    age: int
    # _age: int = field(init=False, default=0)  # Make age private and set a default value
    ssn: str
    phones: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)
    professions: List[str] = field(default_factory=list)

    # @property
    # def age(self):
    #     return self._age
    #
    # @age.setter
    # def age(self, value):
    #     if not isinstance(value, int) or value < 0:
    #         raise ValueError("Invalid age value. Age must be a not negative integer.")
    #     self._age = value

    @classmethod
    def get_persons_from_api(cls, api_url):
        response = requests.get(api_url)

        if response.status_code == 200:
            persons_data = response.json()
            persons_list = []

            for person_data in persons_data:
                person = cls(
                    name=person_data.get('name', ''),
                    age=person_data.get('age', 0),
                    ssn=person_data.get('ssn', ''),
                    phones=person_data.get('phones', []),
                    emails=person_data.get('emails', []),
                    professions=person_data.get('professions', [])
                )
                persons_list.append(person)

            return persons_list
        else:
            raise ValueError(f"Http Error, status_code: {response.status_code}")


if __name__ == '__main__':
    p = Person(name="John Doe", age=30, ssn="123-45-6789")
    p.age = 20
    # p = Person(name="John Doe", ssn="123-45-6789")
