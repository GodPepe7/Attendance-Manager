from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.entities.course_student import CourseStudent
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, QrCodeExpired, AttendanceLoggingException, InvalidInputException
from src.domain.ports.attendance_repository import IAttendanceRepository
from src.domain.ports.clock import IClock
from src.domain.ports.course_repository import ICourseRepository
from src.domain.ports.course_student_repository import ICourseStudentRepository
from src.domain.ports.lecture_repository import ILectureRepository
from src.domain.authorizer_utils import AuthorizerUtils
from src.domain.services.encryption_service import EncryptionService


@dataclass
class IdWrapper:
    user_id: int
    course_id: int
    lecture_id: int


class AttendanceService:
    def __init__(
            self,
            course_student_repo: ICourseStudentRepository,
            lecture_repo: ILectureRepository,
            course_repo: ICourseRepository,
            encryptor: EncryptionService,
            clock: IClock
    ):
        self.course_student_repo = course_student_repo
        self.lecture_repo = lecture_repo
        self.course_repo = course_repo
        self.encryptor = encryptor
        self.clock = clock

    def _get_course_student_and_lecture(self, user: User, lecture_id: int, course_student_id: int) -> (
            CourseStudent, Lecture):
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            raise NotFoundException(f"Lecture with ID {lecture_id} doesn't exist")
        course = self.course_repo.get_by_id(lecture.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        course_student = self.course_student_repo.get_by_id(course_student_id)
        if not course_student:
            raise NotFoundException(f"Course Student with ID {course_student_id} doesn't exist")
        return course_student, lecture

    def save(self, user: User, lecture_id: int, course_student_id: int):
        course_student, lecture = self._get_course_student_and_lecture(user, lecture_id, course_student_id)
        course_student.attended_lectures.add(lecture)
        self.course_student_repo.update(course_student)

    def delete(self, user: User, lecture_id: int, course_student_id: int):
        course_student, lecture = self._get_course_student_and_lecture(user, lecture_id, course_student_id)
        course_student.attended_lectures.remove(lecture)
        self.course_student_repo.update(course_student)

    def generate_qr_code_string(self, user: User, lecture_id: int, seconds: int) -> str:
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            raise NotFoundException(f"Lecture with ID {lecture_id} doesn't exist")
        course = self.course_repo.get_by_id(lecture.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        current_datetime = self.clock.get_current_datetime()
        expiration_time = current_datetime + timedelta(seconds=seconds)
        encrypted_time = self.encryptor.encrypt_lecture_and_time(lecture_id, expiration_time)
        return encrypted_time

    def save_with_qr_code_string(self, user: User, qr_code_string: str) -> None:
        AuthorizerUtils.check_if_role(user, Role.STUDENT)
        current_datetime = self.clock.get_current_datetime()
        lecture_id, expiration_datetime = self.encryptor.decrypt_to_lecture_and_time(qr_code_string)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            raise InvalidInputException("QR code data is malformed")
        if current_datetime > expiration_datetime:
            raise QrCodeExpired("Didn't save attendance. QR Code is already expired")
        course_student = self.course_student_repo.get_by_course_id_and_student_id(lecture.course_id, user.id)
        if not course_student:
            course_student = self.course_student_repo.save_by_course_id_and_user_id(lecture.course_id, user.id)
        course_student.attended_lectures.add(lecture)
        self.course_student_repo.update(course_student)

    def save_with_password(self, user: User, course_id: int, password: str) -> None:
        AuthorizerUtils.check_if_role(user, Role.STUDENT)
        current_datetime = self.clock.get_current_datetime()
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException(f"Course with ID: {course_id} doesn't exist")
        is_valid = course.check_password(password, current_datetime)
        if not is_valid:
            raise AttendanceLoggingException("Password needs to be correct and not expired")
        lecture = self.lecture_repo.get_by_course_id_and_date(course_id, current_datetime.date())
        if not lecture:
            raise NotFoundException(
                f"No lecture with date {current_datetime.date()} for course with ID: {course_id} was found")
        course_student = self.course_student_repo.get_by_course_id_and_student_id(course_id, user.id)
        if not course_student:
            course_student = self.course_student_repo.save_by_course_id_and_user_id(course_id, user.id)
        course_student.attended_lectures.add(lecture)
        self.course_student_repo.update(course_student)
