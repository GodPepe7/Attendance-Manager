import pytest

from src.domain.entities.lecture import Lecture
from src.domain.exceptions import InvalidInputException


def test_lecture_factory_validates_date_input_with_random_string():
    with pytest.raises(InvalidInputException) as exception:
        Lecture.factory(1, "not a date")

    assert "YYYY-MM-DD" in str(exception.value)


def test_lecture_factory_validates_date_input_with_invalid_format():
    with pytest.raises(InvalidInputException) as exception:
        Lecture.factory(1, "1-2-2024")

    assert "YYYY-MM-DD" in str(exception.value)
