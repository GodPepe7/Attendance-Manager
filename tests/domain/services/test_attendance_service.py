import random

import fernet
import pytest

from src.adapters.repositories.attendance_repository_impl import AttendanceRepository
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.lecture import Lecture
from src.domain.services.attendance_service import AttendanceService, IdWrapper
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.encryption_service import EncryptionService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses


class TestAttendanceService:
    @pytest.fixture
    def attendance_service(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        attendance_repo = AttendanceRepository(db_session)
        course_repo = CourseRepository(db_session)
        lecture_repo = LectureRepository(db_session)
        authorizer = AuthorizerService(course_repo, lecture_repo)
        encryptor = EncryptionService(fernet_key=fernet.Fernet.generate_key())
        attendance_service = AttendanceService(attendance_repo, authorizer, encryptor)
        return db_session, attendance_service

    def test_save(self, attendance_service):
        session, attendance_service = attendance_service
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))
        random_enrollment = random.choice(list(random_course.enrolled_students))
        ids = IdWrapper(random_course.professor.id, random_course.id, random_lecture.id)

        attendance_service.save(ids, random_enrollment.id)

        fetched_lecture = session.get(Lecture, random_lecture.id)
        assert random_enrollment in list(fetched_lecture.attended_students)

    def test_delete(self, attendance_service):
        session, attendance_service = attendance_service
        existing_course = self.courses[0]
        existing_lecture = list(existing_course.lectures)[0]
        random_attendance = random.choice(list(existing_lecture.attended_students))
        ids = IdWrapper(existing_course.professor.id, existing_course.id, existing_lecture.id)

        attendance_service.delete(ids, random_attendance.id)

        fetched_lecture = session.get(Lecture, existing_lecture.id)
        assert random_attendance not in list(fetched_lecture.attended_students)
