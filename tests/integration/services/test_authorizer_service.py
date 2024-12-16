import random
import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import UnauthorizedException, NotFoundException
from src.domain.services.authorizer_service import AuthorizerService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses, users


class TestAuthorizerService:
    @pytest.fixture
    def authorizer(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        self.users = [db_session.merge(user) for user in users]
        course_repo = CourseRepository(db_session)
        lecture_repo = LectureRepository(db_session)
        authorizer = AuthorizerService(course_repo, lecture_repo)
        return authorizer

    def test_check_if_professor_of_course_with_course_professor_does_not_raise(self, authorizer):
        existing_course = random.choice(self.courses)

        authorizer.check_if_professor_of_course(existing_course.professor, existing_course.id)

    def test_check_if_professor_of_course_with_not_course_professor(self, authorizer):
        random_course = random.choice(self.courses)
        not_course_professor = User("test", "test@test.test", "test", Role.PROFESSOR, 69420)

        with pytest.raises(UnauthorizedException) as exc:
            authorizer.check_if_professor_of_course(not_course_professor, random_course.id)

        assert "Only the course professor" in str(exc.value)

    def test_check_if_professor_of_lecture_with_lecture_professor_does_not_raise(self, authorizer):
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))

        authorizer.check_if_professor_of_lecture(random_course.professor, random_course.id, random_lecture.id)

    def test_check_if_professor_of_lecture_with_non_lecture_professor_raises(self, authorizer):
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))
        not_course_professor = User("test", "test@test.test", "test", Role.PROFESSOR, 69420)

        with pytest.raises(UnauthorizedException) as exc:
            authorizer.check_if_professor_of_lecture(not_course_professor, random_course.id, random_lecture.id)

        assert "Only the course professor" in str(exc.value)

    def test_check_if_professor_of_lecture_with_non_existing_lecture_raises(self, authorizer):
        random_course = random.choice(self.courses)

        with pytest.raises(NotFoundException) as exc:
            authorizer.check_if_professor_of_lecture(random_course.professor, random_course.id, 23478924)

        assert "doesn't exist" in str(exc.value)

    def test_check_if_professor_of_lecture_with_lecture_of_different_course(self, authorizer):
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))

        with pytest.raises(NotFoundException) as exc:
            authorizer.check_if_professor_of_lecture(random_course.professor, 342124, random_lecture.id)

        assert "not part of the course" in str(exc.value)

    def test_check_if_enrolled_course_student_with_enrolled_student_does_not_raise(self, authorizer):
        random_course = random.choice(self.courses)
        random_enrolled_student = random.choice(list(random_course.enrolled_students)).student

        authorizer.check_if_enrolled_course_student(random_enrolled_student, random_course.id)

    def test_check_if_enrolled_course_student_with_non_enrolled_student_raises(self, authorizer):
        random_course = random.choice(self.courses)
        not_enrolled_student = User("test", "test@test.test", "test", Role.STUDENT, 69420)

        with pytest.raises(UnauthorizedException) as exc:
            authorizer.check_if_enrolled_course_student(not_enrolled_student, random_course.id)

        assert "Only an enrolled student" in str(exc.value)
