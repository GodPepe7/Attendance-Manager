import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.domain.dto import CourseDto
from src.domain.entities.course import Course
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.services.course_service import CourseService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses


class TestCourseService:
    @pytest.fixture
    def course_service(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        course_repo = CourseRepository(db_session)
        course_service = CourseService(course_repo)
        return db_session, course_service

    @staticmethod
    def assert_dto_is_equal_to_course(dto: CourseDto, course: Course):
        # sort to ensure we're iterating over the same element
        lectures = sorted(course.lectures, key=lambda l: l.id)
        lecture_dtos = sorted(dto.lectures, key=lambda l: l.id)
        enrolled_students = sorted(course.enrolled_students, key=lambda es: es.id)
        enrolled_student_dtos = sorted(dto.enrolled_students, key=lambda es: es.id)

        assert dto.id == course.id and dto.name == course.name

        # assert enrolled students of course are equal in dto
        assert len(enrolled_students) == len(enrolled_students)
        for enrolled_student, enrolled_student_dto in zip(enrolled_students, enrolled_student_dtos):
            assert enrolled_student.id == enrolled_student_dto.id
            assert enrolled_student.student.id == enrolled_student_dto.student.id
            assert enrolled_student.student.name == enrolled_student_dto.student.name

        # assert lectures of course are equal in dto
        assert len(lectures) == len(lecture_dtos)
        for lecture, lecture_dto in zip(lectures, lecture_dtos):
            assert lecture.id == lecture_dto.id and lecture.date == lecture_dto.date

            attended_students = sorted(lecture.attended_students, key=lambda a: a.id)
            attended_student_dtos = sorted(lecture_dto.attended_students, key=lambda l: l.id)
            # assert attended_students of lecture are equal in dto
            assert len(attended_students) == len(attended_student_dtos)
            for attended_student, attended_student_dto in zip(attended_students, attended_student_dtos):
                assert attended_student.id == attended_student_dto.id
                assert attended_student.student.id == attended_student_dto.student.id
                assert attended_student.student.name == attended_student_dto.student.name

    def test_get_by_valid_id(self, course_service):
        _, course_service = course_service
        expected_course = self.courses[0]

        dto = course_service.get_by_id(1)

        self.assert_dto_is_equal_to_course(dto, expected_course)

    def test_get_by_not_existing_id(self, course_service):
        _, course_service = course_service

        dto = course_service.get_by_id(999999)

        assert not dto

    def test_get_courses_by_prof_id(self, course_service):
        session, course_service = course_service
        expected_courses = self.courses[:1]

        course_dtos = course_service.get_courses_by_prof_id(2)

        assert len(course_dtos) == 2
        for course, course_dto in zip(expected_courses, course_dtos):
            self.assert_dto_is_equal_to_course(course_dto, course)

    def test_save(self, course_service):
        session, course_service = course_service
        new_course = Course(name="test", professor=User("test_user", "1@test.com", "test", Role.PROFESSOR), id=1234)

        course_id = course_service.save(new_course)

        assert course_id and course_id == 1234
        fetched_course = session.get(Course, course_id)
        assert fetched_course
        assert new_course == fetched_course
