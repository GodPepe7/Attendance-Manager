from datetime import datetime, timedelta

from src.application.entities.course import Course
from src.application.entities.role import Role
from src.application.entities.user import User


class TestCourse:
    
    def test_set_password_hashes_and_can_be_checked(self):
        test_professor = User("test", "test@test.de", "1234", Role.PROFESSOR)
        course = Course(name="test", professor=test_professor)
        new_password = "safe password"
        expiration = datetime(2024, 1, 1, 1, 1, 1)

        course.set_password_and_expiration(new_password, expiration)

        assert course.password_hash != new_password
        before_expiration = expiration - timedelta(seconds=1)
        assert course.check_password(new_password, before_expiration)
