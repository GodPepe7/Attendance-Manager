from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.entities.enrollment import Enrollment
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, QrCodeExpired
from src.domain.ports.attendance_repository import IAttendanceRepository
from src.domain.ports.course_repository import ICourseRepository
from src.domain.ports.enrollment_repository import IEnrollmentRepository
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
            enrollment_repo: IEnrollmentRepository,
            lecture_repo: ILectureRepository,
            course_repo: ICourseRepository,
            encryptor: EncryptionService
    ):
        self.enrollment_repo = enrollment_repo
        self.lecture_repo = lecture_repo
        self.course_repo = course_repo
        self.encryptor = encryptor

    def _get_enrollment_and_lecture(self, user: User, course_id: int, lecture_id: int, enrollment_id: int) -> (
            Enrollment, Lecture):
        course = self.course_repo.get_by_id(course_id)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        AuthorizerUtils.check_if_professor_of_lecture(user, course, lecture)
        enrollment = self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise NotFoundException("Enrollment doesn't exist")
        if enrollment.course_id != course.id:
            raise NotFoundException(
                f"Enrollment with ID '{enrollment.id}' is not part of the course with ID: '{course.id}'!")
        return enrollment, lecture

    def save(self, user: User, course_id: int, lecture_id: int, enrollment_id: int):
        enrollment, lecture = self._get_enrollment_and_lecture(user, course_id, lecture_id, enrollment_id)
        enrollment.attended_lectures.add(lecture)
        self.enrollment_repo.update(enrollment)

    def delete(self, user: User, course_id: int, lecture_id: int, enrollment_id: int):
        enrollment, lecture = self._get_enrollment_and_lecture(user, course_id, lecture_id, enrollment_id)
        enrollment.attended_lectures.remove(lecture)
        self.enrollment_repo.update(enrollment)

    def generate_qr_code_string(self, user: User, course_id: int, lecture_id: int, seconds: int,
                                current_time: datetime) -> str:
        course = self.course_repo.get_by_id(course_id)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        AuthorizerUtils.check_if_professor_of_lecture(user, course, lecture)
        expiration_time = current_time + timedelta(seconds=seconds)
        encrypted_time = self.encryptor.encrypt_date(expiration_time)
        return encrypted_time

    def save_with_qr_code_string(self, user: User, course_id: int, lecture_id: int, qr_code_string: str,
                                 current_time: datetime) -> None:
        AuthorizerUtils.check_if_role(user, Role.STUDENT)
        expiration_time = self.encryptor.decrypt_date(qr_code_string)
        if current_time > expiration_time:
            raise QrCodeExpired("Didn't save attendance. QR Code is already expired")
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            raise NotFoundException("Lecture doesn't exist")
        enrollment = self.enrollment_repo.get_by_course_id_and_student_id(course_id, user.id)
        if not enrollment:
            enrollment = self.enrollment_repo.save_by_course_id_and_user_id(course_id, user.id)
        enrollment.attended_lectures.add(lecture)
        self.enrollment_repo.update(enrollment)
