import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.domain.services.course_service import CourseService


class TestCourseService():

    @pytest.fixture
    def course_service(self, add_courses):
        session, _ = add_courses
        course_repo = CourseRepository(session())
        course_service = CourseService(course_repo)
        return session, course_service
