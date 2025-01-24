import datetime
import random
from datetime import timedelta

import fernet
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.adapters.secondary.clock_impl import Clock
from src.adapters.secondary.course_repository_impl import CourseRepository
from src.adapters.secondary.enrollment_repository_impl import CourseStudentRepository
from src.adapters.secondary.lecture_repository_impl import LectureRepository
from src.domain.entities.course_student import CourseStudent
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, QrCodeExpired, AttendanceLoggingException
from src.domain.services.attendance_service import AttendanceService
from src.domain.services.encryption_service import EncryptionService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import courses


class TestAttendanceService:
    @pytest.fixture
    def attendance_service(self, db_session):
        self.courses = [db_session.merge(course) for course in courses]
        enrollment_repo = CourseStudentRepository(db_session)
        course_repo = CourseRepository(db_session)
        lecture_repo = LectureRepository(db_session)
        encryptor = EncryptionService(fernet_key=fernet.Fernet.generate_key())
        clock = Clock()
        attendance_service = AttendanceService(enrollment_repo, lecture_repo, course_repo, encryptor, clock)
        return db_session, attendance_service

    @staticmethod
    def create_test_student(session: Session):
        new_user = User("new", "new@new.de", "hash", Role.STUDENT)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    def test_save(self, attendance_service):
        session, attendance_service = attendance_service
        random_course = random.choice(self.courses)
        random_lecture = random.choice(list(random_course.lectures))
        random_enrollment = random.choice(list(random_course.students))

        attendance_service.save(random_course.professor, random_course.id, random_lecture.id, random_enrollment.id)

        fetched_enrollment = session.get(CourseStudent, random_enrollment.id)
        assert random_lecture in list(fetched_enrollment.attended_lectures)

    def test_delete(self, attendance_service):
        session, attendance_service = attendance_service
        existing_course = self.courses[0]
        existing_enrollment = list(existing_course.students)[0]
        random_lecture = random.choice(list(existing_enrollment.attended_lectures))

        attendance_service.delete(existing_course.professor, existing_course.id, random_lecture.id,
                                  existing_enrollment.id)

        fetched_enrollment = session.get(CourseStudent, existing_enrollment.id)
        assert random_lecture not in list(fetched_enrollment.attended_lectures)

    def test_delete_non_existing(self, attendance_service):
        _, attendance_service = attendance_service

        existing_course = self.courses[0]
        existing_lecture = list(existing_course.lectures)[0]

        with pytest.raises(NotFoundException) as exc:
            attendance_service.delete(existing_course.professor, existing_course.id, existing_lecture.id, 1234)

        assert "doesn't exist" in str(exc)

    def test_generate_qr_then_scan_works(self, attendance_service):
        session, attendance_service = attendance_service
        course = self.courses[1]
        enrollment = list(course.students)[0]
        lecture = list(course.lectures)[0]
        EXPIRATION_TIME = 30
        assert lecture not in list(enrollment.attended_lectures)

        qr_code_str = attendance_service.generate_qr_code_string(course.professor, course.id, lecture.id,
                                                                 EXPIRATION_TIME)
        attendance_service.save_with_qr_code_string(enrollment.student, qr_code_str)

        updated_enrollment = session.get(CourseStudent, enrollment.id)
        assert lecture in list(updated_enrollment.attended_lectures)

    def test_generate_qr_then_scan_expired_raises(self, attendance_service, mocker):
        _, attendance_service = attendance_service
        course = self.courses[1]
        enrollment = list(course.students)[0]
        lecture = list(course.lectures)[0]
        EXPIRATION_TIME = 30
        thirty_one_seconds_after = datetime.datetime.now() + datetime.timedelta(seconds=31)

        qr_code_str = attendance_service.generate_qr_code_string(course.professor, course.id, lecture.id,
                                                                 EXPIRATION_TIME)
        with pytest.raises(QrCodeExpired) as exc:
            # mock get_current_datetime to return a datetime past the expiration time
            mocker.patch.object(attendance_service.clock, "get_current_datetime", return_value=thirty_one_seconds_after)
            attendance_service.save_with_qr_code_string(enrollment.student, qr_code_str)

        assert "expired" in str(exc.value)

    def test_generate_qr_then_scan_with_not_yet_enrolled_student_also_works(self, attendance_service):
        session, attendance_service = attendance_service
        new_user = self.create_test_student(session)
        existing_course = random.choice(self.courses)
        existing_lecture = random.choice(list(existing_course.lectures))
        EXPIRATION_TIME = 30

        qr_code_str = attendance_service.generate_qr_code_string(existing_course.professor, existing_course.id,
                                                                 existing_lecture.id,
                                                                 EXPIRATION_TIME)
        attendance_service.save_with_qr_code_string(new_user, qr_code_str)

        stmt = select(CourseStudent).where(CourseStudent.course_id == existing_course.id,
                                           CourseStudent.student_id == new_user.id)
        updated_enrollment = session.execute(stmt).scalar()
        assert updated_enrollment
        assert existing_lecture in updated_enrollment.attended_lectures

    def test_save_with_correct_password_saves_to_db(self, attendance_service, mocker):
        session, attendance_service = attendance_service
        new_user = self.create_test_student(session)
        existing_course = self.courses[0]
        course_password = "1234"
        valid_datetime = existing_course.password_expiration_datetime - timedelta(minutes=30)
        mocker.patch.object(attendance_service.clock, "get_current_datetime",
                            return_value=valid_datetime)

        attendance_service.save_with_password(new_user, existing_course.id, course_password)

        stmt = select(CourseStudent).where(CourseStudent.course_id == existing_course.id,
                                           CourseStudent.student_id == new_user.id)
        course_student = session.execute(stmt).scalar()
        expected_lecture = Lecture(id=2, course_id=1, date=datetime.date(2024, 12, 25))
        assert course_student
        assert expected_lecture in course_student.attended_lectures, "Lecture hasn't been added to attended lecture list of course student"

    def test_save_with_wrong_password_raises(self, attendance_service):
        session, attendance_service = attendance_service
        new_user = self.create_test_student(session)
        existing_course = self.courses[0]
        wrong_password = "wrong_password"

        with pytest.raises(AttendanceLoggingException) as exc:
            attendance_service.save_with_password(new_user, existing_course.id, wrong_password)

        assert exc

    def test_save_with_expired_password_raises(self, attendance_service, mocker):
        session, attendance_service = attendance_service
        new_user = self.create_test_student(session)
        existing_course = self.courses[0]
        wrong_password = "1234"
        two_hours_after_expiration = existing_course.password_expiration_datetime + timedelta(hours=2)

        with pytest.raises(AttendanceLoggingException) as exc:
            mocker.patch.object(attendance_service.clock, "get_current_datetime",
                                return_value=two_hours_after_expiration)
            attendance_service.save_with_password(new_user, existing_course.id, wrong_password)

        assert exc
