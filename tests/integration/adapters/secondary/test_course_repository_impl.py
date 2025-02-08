import random

import pytest

from src.adapters.secondary.course_repository_impl import CourseRepository
from src.application.entities.course import Course
from src.application.entities.course_student import CourseStudent
from src.application.entities.lecture import Lecture
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import DuplicateException
from tests.fixtures import engine, tables, add_data, db_session
from tests.test_data import courses


class TestCourseRepo:

    @pytest.fixture
    def course_repo(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        return CourseRepository(db_session)

    def test_get_by_id_gives_full_course_with_all_lectures_and_students(self, course_repo):
        existing_course = random.choice(self.courses)

        course_from_db = course_repo.get_by_id(existing_course.id)

        assert existing_course == course_from_db
        assert existing_course.lectures == course_from_db.lectures
        assert existing_course.students == course_from_db.students

    def test_save(self, course_repo):
        professor = User("max", "max@email.com", "blub", Role.PROFESSOR)
        course = Course("Math for Dummies", professor)

        id = course_repo.save(course)

        saved_course = course_repo.session.get(Course, id)
        assert course == saved_course

    def test_save_with_already_existing_course_name_raises(self, course_repo):
        already_existing_course_name = random.choice(self.courses).name
        professor = User("max", "max@email.com", "blub", Role.PROFESSOR, 100)
        course = Course(already_existing_course_name, professor)

        with pytest.raises(DuplicateException) as e:
            course_repo.save(course)

        assert e

    def test_update_course_to_already_existing_course_name(self, course_repo):
        existing_course = self.courses[0]
        other_course_name = self.courses[1].name

        existing_course.name = other_course_name
        with pytest.raises(DuplicateException) as e:
            course_repo.update(existing_course)

        assert e

    def test_delete_also_cascades_to_related_tables(self, course_repo):
        existing_course = self.courses[0]
        lectures = list(existing_course.lectures)
        course_students = list(existing_course.students)

        course_repo.delete(existing_course)

        course = course_repo.session.get(Course, existing_course.id)
        assert not course
        assert len(lectures) != 0
        for lecture in lectures:
            lecture_from_db = course_repo.session.get(Lecture, lecture.id)
            assert not lecture_from_db

        assert len(course_students) != 0
        for course_student in course_students:
            course_student_from_db = course_repo.session.get(CourseStudent, course_student.id)
            assert not course_student_from_db
