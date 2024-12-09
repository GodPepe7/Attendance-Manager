import datetime
import random

import pytest

from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.lecture import Lecture
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.lecture_service import LectureService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses


class TestLectureService:
    @pytest.fixture
    def lecture_service(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        lecture_repo = LectureRepository(db_session)
        course_repo = CourseRepository(db_session)
        authorizer = AuthorizerService(course_repo, lecture_repo)
        lecture_service = LectureService(lecture_repo, authorizer)
        return db_session, lecture_service

    def test_save(self, lecture_service):
        session, lecture_service = lecture_service
        random_course = random.choice(self.courses)
        lecture = Lecture(
            course_id=random_course.id,
            date=datetime.date.today(),
        )

        lecture_id = lecture_service.save(lecture, random_course.professor.id)

        assert lecture_id
        fetched_lecture = session.get(Lecture, lecture_id)
        assert fetched_lecture
        assert fetched_lecture == lecture

    def test_delete(self, lecture_service):
        session, lecture_service = lecture_service
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))

        lecture_service.delete(random_lecture.id, random_lecture.course_id, random_course.professor.id)

        fetched_lecture = session.get(Lecture, random_lecture.id)
        assert not fetched_lecture
