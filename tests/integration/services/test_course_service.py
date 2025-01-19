import datetime
import random

import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.domain.dto import CourseResponseDto, UpdateCoursePasswordRequestDto
from src.domain.entities.course import Course
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, UnauthorizedException
from src.domain.services.course_service import CourseService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses, users


class TestCourseService:
    @pytest.fixture
    def course_service(self, db_session):
        self.users = [db_session.merge(user) for user in users]
        self.courses = [db_session.merge(course) for course in courses]
        course_repo = CourseRepository(db_session)
        course_service = CourseService(course_repo)
        return db_session, course_service

    @staticmethod
    def assert_dto_is_equal_to_course(dto: CourseResponseDto, course: Course):
        # sort to ensure we're iterating over the same element
        lectures = sorted(course.lectures, key=lambda l: l.id)
        lecture_dtos = sorted(dto.lectures, key=lambda l: l.id)
        course_students = sorted(course.students, key=lambda es: es.id)
        course_students_dtos = sorted(dto.students, key=lambda es: es.id)

        assert dto.id == course.id and dto.name == course.name

        # assert lectures of course are equal to dto
        assert len(lectures) == len(lecture_dtos)
        for lecture, lecture_dto in zip(lectures, lecture_dtos):
            assert lecture.id == lecture_dto.id
            assert lecture.date == lecture_dto.date

        # assert enrolled_student of course are equal to dto
        assert len(course_students) == len(course_students_dtos)
        for enrollment, enrollment_dto in zip(course_students, course_students_dtos):
            assert enrollment.id == enrollment_dto.id

            attended_lectures = sorted(enrollment.attended_lectures, key=lambda lec: lec.id)
            attended_lectures_dtos = sorted(enrollment_dto.attended_lectures, key=lambda lec: lec.id)
            # assert attended_lectures of enrollment are equal to dto
            assert len(attended_lectures) == len(attended_lectures_dtos)
            for attended_lecture, attended_lecture_dto in zip(attended_lectures, attended_lectures_dtos):
                assert attended_lecture.id == attended_lecture_dto.id
                assert attended_lecture.date == attended_lecture_dto.date

    def test_get_by_id_with_existing_course_id_and_user_is_the_course_professor_returns_course(self, course_service):
        _, course_service = course_service
        existing_course = random.choice(self.courses)

        dto = course_service.get_by_id(existing_course.professor, existing_course.id)

        self.assert_dto_is_equal_to_course(dto, existing_course)

    def test_get_by_id_with_existing_course_id_and_user_is_not_the_course_professor_raises(self, course_service):
        _, course_service = course_service
        existing_course = random.choice(self.courses)
        new_prof = User("foo", "foo@bar.com", "foo", Role.PROFESSOR, 69420)

        with pytest.raises(UnauthorizedException) as exc:
            course_service.get_by_id(new_prof, existing_course.id)

        assert "Only the course professor" in str(exc.value)

    def test_get_by_non_existing_course_id_raises(self, course_service):
        _, course_service = course_service
        non_existing_course_id = 69420
        new_prof = User("foo", "foo@bar.com", "foo", Role.PROFESSOR, 69420)

        with pytest.raises(NotFoundException) as exc:
            course_service.get_by_id(new_prof, non_existing_course_id)

        assert "doesn't exist" in str(exc.value)

    def test_get_courses_by_prof_id_returns_all_courses_of_professor(self, course_service):
        session, course_service = course_service
        existing_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])
        expected_courses = [course for course in self.courses if course.professor.id == existing_professor.id]

        course_dtos = course_service.get_courses_by_prof(existing_professor)

        assert len(course_dtos) == len(expected_courses)
        course_dtos.sort(key=lambda course: course.id)
        for course, course_dto in zip(expected_courses, course_dtos):
            self.assert_dto_is_equal_to_course(course_dto, course)

    def test_save_course_persists_to_db(self, course_service):
        session, course_service = course_service
        existing_prof = random.choice([user for user in self.users if user.role == Role.PROFESSOR])
        new_course = Course(name="test", professor=existing_prof)

        course_id = course_service.save(existing_prof, new_course)

        assert course_id
        fetched_course = session.get(Course, course_id)
        assert fetched_course
        assert new_course == fetched_course

    def test_update_password_not_saved_as_clear_text(self, course_service):
        session, course_service = course_service
        existing_course = random.choice(self.courses)
        password = "1234"
        course_dto = UpdateCoursePasswordRequestDto(existing_course.id, password, datetime.datetime.now())

        course_service.update_password(existing_course.professor, course_dto)

        fetched_course = session.get(Course, existing_course.id)
        assert fetched_course.password_hash != password
