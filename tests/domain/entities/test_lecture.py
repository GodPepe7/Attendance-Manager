import pytest

from src.domain.entities.lecture import Lecture
from src.domain.exceptions import InvalidInputException


class TestLecture:

    def test_lecture_factory_validates_date_input_with_random_string(self):
        with pytest.raises(InvalidInputException) as exception:
            Lecture.factory(1, "not a date")

        assert "YYYY-MM-DD" in str(exception.value)

    def test_lecture_factory_validates_date_input_with_invalid_format(self):
        with pytest.raises(InvalidInputException) as exception:
            Lecture.factory(1, "1-2-2024")

        assert "YYYY-MM-DD" in str(exception.value)

    def test_lecture_factory_validates_date_input_with_invalid_date(self):
        with pytest.raises(InvalidInputException) as exception:
            Lecture.factory(1, "9999-15-67")

        assert "needs to be valid" in str(exception.value)
