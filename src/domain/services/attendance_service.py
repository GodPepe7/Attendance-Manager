from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.entities.enrollment import Enrollment
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, QrCodeExpired
from src.domain.ports.attendance_repository import IAttendanceRepository
from src.domain.ports.enrollment_repository import IEnrollmentRepository
from src.domain.ports.user_repository import IUserRepository
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.encryption_service import EncryptionService


@dataclass
class IdWrapper:
    user_id: int
    course_id: int
    lecture_id: int


class AttendanceService:
    def __init__(
            self,
            attendance_repo: IAttendanceRepository,
            enrollment_repo: IEnrollmentRepository,
            authorizer: AuthorizerService,
            encryptor: EncryptionService
    ):
        self.repo = attendance_repo
        self.enrollment_repo = enrollment_repo
        self.authorizer = authorizer
        self.encryptor = encryptor

    def save(self, user: User, course_id: int, lecture_id: int, enrollment_id: int):
        self.authorizer.check_if_professor_of_lecture(user, course_id, lecture_id)
        saved = self.repo.save(lecture_id, enrollment_id)
        if not saved:
            raise NotFoundException(
                f"Enrolled student of the given lecture's course doesn't exist")

    def delete(self, user: User, course_id: int, lecture_id: int, enrollment_id: int):
        self.authorizer.check_if_professor_of_lecture(user, course_id, lecture_id)
        deleted = self.repo.delete(lecture_id, enrollment_id)
        if not deleted:
            raise NotFoundException(
                f"Enrolled student of the given lecture's course doesn't exist")

    def generate_qr_code_string(self, user: User, course_id: int, lecture_id: int, seconds: int,
                                current_time: datetime) -> str:
        self.authorizer.check_if_professor_of_lecture(user, course_id, lecture_id)
        expiration_time = current_time + timedelta(seconds=seconds)
        encrypted_time = self.encryptor.encrypt_date(expiration_time)
        return encrypted_time

    def save_with_qr_code_string(self, user: User, course_id: int, lecture_id: int, qr_code_string: str,
                                 current_time: datetime) -> None:
        self.authorizer.check_if_role(user, Role.STUDENT)
        expiration_time = self.encryptor.decrypt_date(qr_code_string)
        if current_time > expiration_time:
            raise QrCodeExpired("Didn't save attendance. QR Code is already expired")
        enrollment = self.enrollment_repo.get_by_course_id_and_student_id(course_id, user.id)
        if not enrollment:
            enrollment = self.enrollment_repo.save_by_course_id_and_student_id(course_id, user.id)
        saved = self.repo.save(lecture_id, enrollment.id)
        if not saved:
            raise NotFoundException(
                f"Lecture with ID: {lecture_id} doesn't exist")
