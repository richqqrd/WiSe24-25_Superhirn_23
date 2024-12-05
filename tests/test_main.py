# tests/test_main.py

import pytest
from src.main import add, subtract

def test_add():
    """Testet die Funktion add."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    """Testet die Funktion subtract."""
    assert subtract(5, 2) == 3
    assert subtract(0, 5) == -5
    assert subtract(-3, -2) == -1
    assert subtract(3, 2) == 1

if __name__ == "__main__":
    pytest.main()
