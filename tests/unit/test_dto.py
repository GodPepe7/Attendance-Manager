import pytest

from src.application.dto import UpdateCourseRequestDto
from src.application.exceptions import InvalidInputException


class TestDto:
    def test_update_course_request_creation_raises_when_password_present_but_no_expiration_datetime(self):
        password = "test"

        with pytest.raises(InvalidInputException) as exc:
            UpdateCourseRequestDto.factory(1, None, password, None)

        assert exc

    def test_update_course_request_creation_raises_when_no_password_present_but_expiration_datetime(self):
        expiration_datetime = "2025-01-01T12:30"

        with pytest.raises(InvalidInputException) as exc:
            UpdateCourseRequestDto.factory(1, None, None, expiration_datetime)

        assert exc
