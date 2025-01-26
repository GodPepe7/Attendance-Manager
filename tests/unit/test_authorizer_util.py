import random
import pytest

from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import UnauthorizedException, NotFoundException
from src.domain.authorizer_utils import AuthorizerUtils
from tests.test_data import courses, users


class TestAuthorizerService:
    courses = courses
    users = users

    def test_check_if_professor_of_course_with_course_professor_does_not_raise(self):
        existing_course = random.choice(self.courses)

        AuthorizerUtils.check_if_professor_of_course(existing_course.professor, existing_course)

    def test_check_if_professor_of_course_with_none_raises(self):
        some_professor = User("test", "test@test.test", "test", Role.PROFESSOR, 69420)

        with pytest.raises(NotFoundException) as exc:
            AuthorizerUtils.check_if_professor_of_course(some_professor, None)

        assert exc.value

    def test_check_if_professor_of_course_with_not_course_professor_raises(self):
        random_course = random.choice(self.courses)
        not_course_professor = User("test", "test@test.test", "test", Role.PROFESSOR, 69420)

        with pytest.raises(UnauthorizedException) as exc:
            AuthorizerUtils.check_if_professor_of_course(not_course_professor, random_course)

        assert "Only the course professor" in str(exc.value)
