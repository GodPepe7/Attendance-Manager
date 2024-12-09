import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.exceptions import UnauthorizedException, NotFoundException
from src.domain.services.authorizer_service import AuthorizerService
from tests.conftest import engine, tables, add_data, db_session


class TestAuthorizerService:
    @pytest.fixture
    def authorizer(self, db_session):
        course_repo = CourseRepository(db_session)
        lecture_repo = LectureRepository(db_session)
        authorizer = AuthorizerService(course_repo, lecture_repo)
        return authorizer

    def test_authorized_course_professor(self, authorizer):
        authorizer.is_professor_of_course(2, 1)

    def test_not_course_professor(self, authorizer):
        with pytest.raises(UnauthorizedException) as exc:
            authorizer.is_professor_of_course(1, 1)

        assert "Only the course professor" in str(exc.value)

    def test_authorized_lecture_professor(self, authorizer):
        authorizer.is_professor_of_lecture(2, 2, 3)

    def test_not_lecture_professor(self, authorizer):
        with pytest.raises(UnauthorizedException) as exc:
            authorizer.is_professor_of_lecture(1, 2, 3)

        assert "Only the course professor" in str(exc.value)

    def test_not_course_lecture(self, authorizer):
        with pytest.raises(NotFoundException) as exc:
            authorizer.is_professor_of_lecture(1, 1, 3)

        assert "not part of the course" in str(exc.value)

    def test_authorized_enrolled_course_student(self, authorizer):
        authorizer.is_enrolled_course_student(1, 1)

    def test_not_enrolled_student(self, authorizer):
        with pytest.raises(UnauthorizedException) as exc:
            authorizer.is_enrolled_course_student(3, 2)

        assert "Only an enrolled student" in str(exc.value)
