from datetime import datetime, timedelta

from src.domain.exceptions import NotAuthorizedException, NotFoundException, QrCodeExpired
from src.domain.ports.attendance_repository import IAttendanceRepository
from src.domain.ports.auth_repository import IAuthRepository
from src.domain.services.encryption_service import EncryptionService


class AttendanceService:
    def __init__(self, attendance_repo: IAttendanceRepository, auth_repo: IAuthRepository,
                 encryption_service: EncryptionService):
        self.repo = attendance_repo
        self.auth_repo = auth_repo
        self.encryption_service = encryption_service

    def __authorize_only_prof(self, prof_id: int, course_id: int):
        is_course_professor = self.auth_repo.is_course_professor(prof_id, course_id)
        if not is_course_professor:
            raise NotAuthorizedException(
                "Couldn't save attendance. Only the course professor is authorized to do so!")

    def __authorize_only_student(self, student_id: int, course_id: int):
        is_course_professor = self.auth_repo.is_course_student(student_id, course_id)
        if not is_course_professor:
            raise NotAuthorizedException(
                "Couldn't save attendance. Only the student themself is authorized to do so!")

    def save(self, prof_id: int, lecture_id: int, course_id: int, student_id: int):
        self.__authorize_only_prof(prof_id, course_id)
        saved = self.repo.save(lecture_id, student_id)
        if not saved:
            raise NotFoundException(
                f"Couldn't save attendance. Lecture with ID: {lecture_id} in Course with ID: {course_id} doesn't exist")

    def delete(self, prof_id: int, lecture_id: int, course_id: int, student_id: int):
        self.__authorize_only_prof(prof_id, course_id)
        deleted = self.repo.delete(lecture_id, student_id)
        if not deleted:
            raise NotFoundException(
                f"Couldn't delete attendance. Attendance of student with ID: {student_id} in lecture with ID: {lecture_id} doesn't exist")

    def generate_qr_code_string(self, prof_id: int, course_id: int, seconds: int, current_time: datetime):
        self.__authorize_only_prof(prof_id, course_id)
        expiration_time = current_time + timedelta(seconds=seconds)
        encrypted_time = self.encryption_service.encrypt_date(expiration_time)
        return encrypted_time

    def save_with_qr_code_string(self, student_id: int, course_id: int, lecture_id: int, qr_code_string: str,
                                 current_time: datetime):
        self.__authorize_only_student(student_id, course_id)
        expiration_time = self.encryption_service.decrypt_date(qr_code_string)
        if current_time > expiration_time:
            raise QrCodeExpired("Couldn't save attendance. QR Code is already expired")
        saved = self.repo.save(lecture_id, student_id)
        if not saved:
            raise NotFoundException(
                f"Couldn't save attendance. Lecture with ID: {lecture_id} in Course with ID: {course_id} doesn't exist")
