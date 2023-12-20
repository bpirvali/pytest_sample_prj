import pytest
import src.my_functions as my_functions


def test_add():
    r = my_functions.add(1, 4)
    assert r == 5

