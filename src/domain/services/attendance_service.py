from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.exceptions import NotFoundException, QrCodeExpired
from src.domain.ports.attendance_repository import IAttendanceRepository
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.encryption_service import EncryptionService


@dataclass
class IdWrapper:
    user_id: int
    course_id: int
    lecture_id: int


class AttendanceService:
    def __init__(self, attendance_repo: IAttendanceRepository,
                 authorizer: AuthorizerService,
                 encryptor: EncryptionService):
        self.repo = attendance_repo
        self.authorizer = authorizer
        self.encryptor = encryptor

    def save(self, ids: IdWrapper, enrollment_id: int):
        self.authorizer.is_professor_of_lecture(ids.user_id, ids.course_id, ids.lecture_id)
        saved = self.repo.save(ids.lecture_id, enrollment_id)
        if not saved:
            raise NotFoundException(
                f"Couldn't save attendance. Needs to be an enrolled student of the given lecture's course")

    def delete(self, ids: IdWrapper, enrollment_id: int):
        self.authorizer.is_professor_of_lecture(ids.user_id, ids.course_id, ids.lecture_id)
        deleted = self.repo.delete(ids.lecture_id, enrollment_id)
        if not deleted:
            raise NotFoundException(
                f"Couldn't delete attendance. Attendancy for the given lecture doesn't exist!")

    def generate_qr_code_string(self, ids: IdWrapper, seconds: int,
                                current_time: datetime):
        self.authorizer.is_professor_of_lecture(ids.user_id, ids.course_id, ids.lecture_id)
        expiration_time = current_time + timedelta(seconds=seconds)
        encrypted_time = self.encryptor.encrypt_date(expiration_time)
        return encrypted_time

    def save_with_qr_code_string(self, ids: IdWrapper, qr_code_string: str,
                                 current_time: datetime):
        self.authorizer.is_enrolled_course_student(ids.user_id, ids.course_id)
        expiration_time = self.encryptor.decrypt_date(qr_code_string)
        if current_time > expiration_time:
            raise QrCodeExpired("Didn't save attendance. QR Code is already expired")
        saved = self.repo.save(ids.lecture_id, ids.user_id)
        if not saved:
            raise NotFoundException(
                f"Couldn't save attendance. Student and lecture need to exist!")
