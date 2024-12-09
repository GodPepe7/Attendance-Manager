import datetime
import random

import fernet
import pytest

from src.adapters.repositories.attendance_repository_impl import AttendanceRepository
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.enrollment_repository_impl import EnrollmentRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.enrollment import Enrollment
from src.domain.exceptions import NotFoundException, QrCodeExpired
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
        enrollment_repo = EnrollmentRepository(db_session)
        course_repo = CourseRepository(db_session)
        lecture_repo = LectureRepository(db_session)
        authorizer = AuthorizerService(course_repo, lecture_repo)
        encryptor = EncryptionService(fernet_key=fernet.Fernet.generate_key())
        attendance_service = AttendanceService(attendance_repo, enrollment_repo, authorizer, encryptor)
        return db_session, attendance_service

    def test_save(self, attendance_service):
        session, attendance_service = attendance_service
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))
        random_enrollment = random.choice(list(random_course.enrolled_students))
        ids = IdWrapper(random_course.professor.id, random_course.id, random_lecture.id)

        attendance_service.save(ids, random_enrollment.id)

        fetched_enrollment = session.get(Enrollment, random_enrollment.id)
        assert random_lecture in list(fetched_enrollment.attended_lectures)

    def test_save_not_enrolled_student(self, attendance_service):
        _, attendance_service = attendance_service
        existing_course = self.courses[1]
        existing_lecture = list(existing_course.lectures)[0]
        not_enrolled_student = list(self.courses[0].enrolled_students)[0]
        ids = IdWrapper(existing_course.professor.id, existing_course.id, existing_lecture.id)

        with pytest.raises(NotFoundException) as exc:
            attendance_service.save(ids, not_enrolled_student.id)

        assert "Needs to be an enrolled student" in str(exc.value)

    def test_delete(self, attendance_service):
        session, attendance_service = attendance_service
        existing_course = self.courses[0]
        existing_enrollment = list(existing_course.enrolled_students)[0]
        random_lecture = random.choice(list(existing_enrollment.attended_lectures))
        ids = IdWrapper(existing_course.professor.id, existing_course.id, random_lecture.id)

        attendance_service.delete(ids, existing_enrollment.id)

        fetched_enrollment = session.get(Enrollment, existing_enrollment.id)
        assert random_lecture not in list(fetched_enrollment.attended_lectures)

    def test_delete_non_existing(self, attendance_service):
        _, attendance_service = attendance_service

        existing_course = self.courses[0]
        existing_lecture = list(existing_course.lectures)[0]
        ids = IdWrapper(existing_course.professor.id, existing_course.id, existing_lecture.id)

        with pytest.raises(NotFoundException) as exc:
            attendance_service.delete(ids, 1234)

        assert "doesn't exist" in str(exc)

    def test_generate_qr_then_scan(self, attendance_service):
        session, attendance_service = attendance_service
        course = self.courses[1]
        enrollment = list(course.enrolled_students)[0]
        lecture = list(course.lectures)[0]
        professor_ids = IdWrapper(course.professor.id, course.id, lecture.id)
        student_ids = IdWrapper(enrollment.student.id, course.id, lecture.id)
        EXPIRATION_TIME = 30
        assert lecture not in list(enrollment.attended_lectures)

        qr_code_str = attendance_service.generate_qr_code_string(professor_ids, EXPIRATION_TIME,
                                                                 datetime.datetime.now())
        attendance_service.save_with_qr_code_string(student_ids, qr_code_str, datetime.datetime.now())

        updated_enrollment = session.get(Enrollment, enrollment.id)
        assert lecture in list(updated_enrollment.attended_lectures)

    def test_generate_qr_then_scan_expired(self, attendance_service):
        _, attendance_service = attendance_service
        course = self.courses[1]
        enrollment = list(course.enrolled_students)[0]
        lecture = list(course.lectures)[0]
        professor_ids = IdWrapper(course.professor.id, course.id, lecture.id)
        student_ids = IdWrapper(enrollment.student.id, course.id, lecture.id)
        EXPIRATION_TIME = 30
        now = datetime.datetime.now()
        thirty_one_seconds_after = now + datetime.timedelta(seconds=31)

        qr_code_str = attendance_service.generate_qr_code_string(professor_ids, EXPIRATION_TIME, now)
        with pytest.raises(QrCodeExpired) as exc:
            attendance_service.save_with_qr_code_string(student_ids, qr_code_str, thirty_one_seconds_after)

        assert "expired" in str(exc.value)
