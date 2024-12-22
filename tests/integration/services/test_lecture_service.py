import datetime
import random

import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
from src.domain.services.lecture_service import LectureService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses


class TestLectureService:
    @pytest.fixture
    def lecture_service(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        lecture_repo = LectureRepository(db_session)
        course_repo = CourseRepository(db_session)
        lecture_service = LectureService(lecture_repo, course_repo)
        return db_session, lecture_service

    def test_save_lecture_persists_in_db(self, lecture_service):
        session, lecture_service = lecture_service
        random_course = random.choice(self.courses)
        lecture = Lecture(
            course_id=random_course.id,
            date=datetime.date.today(),
        )

        lecture_id = lecture_service.save(random_course.professor, lecture)

        assert lecture_id
        fetched_lecture = session.get(Lecture, lecture_id)
        assert fetched_lecture
        assert fetched_lecture == lecture

    def test_save_to_non_existing_course_raises(self, lecture_service):
        session, lecture_service = lecture_service
        test_prof = User("test", "test@test.test", "test", Role.PROFESSOR)
        lecture = Lecture(
            course_id=69420,
            date=datetime.date.today(),
        )

        with pytest.raises(NotFoundException) as exc:
            lecture_service.save(test_prof, lecture)

        assert "doesn't exist" in str(exc.value)

    def test_deleting_existing_lecture_removes_from_db(self, lecture_service):
        session, lecture_service = lecture_service
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))

        lecture_service.delete(random_course.professor, random_lecture.course_id, random_lecture.id)

        fetched_lecture = session.get(Lecture, random_lecture.id)
        assert not fetched_lecture

    def test_delete_lecture_not_belonging_to_course_raises(self, lecture_service):
        _, lecture_service = lecture_service
        random_course = random.choice(self.courses)
        non_existing_lecture = 69420

        with pytest.raises(NotFoundException) as exc:
            lecture_service.delete(random_course.professor, random_course.id, non_existing_lecture)

        assert "doesn't exist" in str(exc.value)

    def test_update_existing_lecture_persists_in_db(self, lecture_service):
        session, lecture_service = lecture_service
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))
        new_date = datetime.datetime.now().date()

        lecture_service.update(random_course.professor, random_course.id, random_lecture.id, new_date)

        fetched_lecture = session.get(Lecture, random_lecture.id)
        assert fetched_lecture.date == new_date
