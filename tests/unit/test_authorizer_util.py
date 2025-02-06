import copy
import random
import pytest

from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import UnauthorizedException, NotFoundException
from src.application.authorizer_utils import AuthorizerUtils
from tests.test_data import courses, users


class TestAuthorizerService:
    courses = courses
    users = users

    def test_check_if_professor_of_course_with_course_professor_does_not_raise(self):
        existing_course = random.choice(self.courses)
        professor_copy = copy.deepcopy(existing_course.professor)

        AuthorizerUtils.check_if_professor_of_course(professor_copy, existing_course)

    def test_check_if_professor_of_course_with_not_course_professor_raises(self):
        random_course = random.choice(self.courses)
        not_course_professor = User("test", "test@test.test", "test", Role.PROFESSOR, 69420)

        with pytest.raises(UnauthorizedException) as exc:
            AuthorizerUtils.check_if_professor_of_course(not_course_professor, random_course)

        assert "Only the course professor" in str(exc.value)
