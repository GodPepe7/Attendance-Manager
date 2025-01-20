from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.entities.course_student import CourseStudent
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, QrCodeExpired, AttendanceLoggingException
from src.domain.ports.attendance_repository import IAttendanceRepository
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
            encryptor: EncryptionService
    ):
        self.course_student_repo = course_student_repo
        self.lecture_repo = lecture_repo
        self.course_repo = course_repo
        self.encryptor = encryptor

    def _get_course_student_and_lecture(self, user: User, course_id: int, lecture_id: int, course_student_id: int) -> (
            CourseStudent, Lecture):
        course = self.course_repo.get_by_id(course_id)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        AuthorizerUtils.check_if_professor_of_lecture(user, course, lecture)
        course_student = self.course_student_repo.get_by_id(course_student_id)
        if not course_student:
            raise NotFoundException("course_student doesn't exist")
        return course_student, lecture

    def save(self, user: User, course_id: int, lecture_id: int, course_student_id: int):
        course_student, lecture = self._get_course_student_and_lecture(user, course_id, lecture_id, course_student_id)
        course_student.attended_lectures.add(lecture)
        self.course_student_repo.update(course_student)

    def delete(self, user: User, course_id: int, lecture_id: int, course_student_id: int):
        course_student, lecture = self._get_course_student_and_lecture(user, course_id, lecture_id, course_student_id)
        course_student.attended_lectures.remove(lecture)
        self.course_student_repo.update(course_student)

    def generate_qr_code_string(self, user: User, course_id: int, lecture_id: int, seconds: int,
                                current_time: datetime) -> str:
        course = self.course_repo.get_by_id(course_id)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        AuthorizerUtils.check_if_professor_of_lecture(user, course, lecture)
        expiration_time = current_time + timedelta(seconds=seconds)
        encrypted_time = self.encryptor.encrypt_lecture_and_time(lecture_id, expiration_time)
        return encrypted_time

    def save_with_qr_code_string(self, user: User, qr_code_string: str,
                                 current_time: datetime = datetime.now()) -> None:
        AuthorizerUtils.check_if_role(user, Role.STUDENT)
        lecture_id, expiration_time = self.encryptor.decrypt_to_lecture_and_time(qr_code_string)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            raise NotFoundException("Lecture doesn't exist")
        if current_time > expiration_time:
            raise QrCodeExpired("Didn't save attendance. QR Code is already expired")
        course_student = self.course_student_repo.get_by_course_id_and_student_id(lecture.course_id, user.id)
        if not course_student:
            course_student = self.course_student_repo.save_by_course_id_and_user_id(lecture.course_id, user.id)
        course_student.attended_lectures.add(lecture)
        self.course_student_repo.update(course_student)

    def save_with_password(self, user: User, course_id: int, password: str,
                           current_datetime: datetime = datetime.now()) -> None:
        AuthorizerUtils.check_if_role(user, Role.STUDENT)
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException(f"Course with ID: {course_id} doesn't exist")
        is_valid = course.check_password(password, current_datetime)
        if not is_valid:
            raise AttendanceLoggingException("Couldn't log attendance. Password is either incorrect or already expired")
        lecture = self.lecture_repo.get_by_course_id_and_date(course_id, current_datetime.date())
        if not lecture:
            raise NotFoundException(
                f"No lecture with date {current_datetime.date()} for course with ID: {course_id} was found")
        course_student = self.course_student_repo.get_by_course_id_and_student_id(course_id, user.id)
        if not course_student:
            course_student = self.course_student_repo.save_by_course_id_and_user_id(course_id, user.id)
        course_student.attended_lectures.add(lecture)
        self.course_student_repo.update(course_student)
