from src.domain.exceptions import NotAuthorizedException, NotFoundException
from src.domain.ports.attendance_repository import IAttendanceRepository
from src.domain.ports.auth_repository import IAuthRepository


class AttendanceService:
    def __init__(self, attendance_repo: IAttendanceRepository, auth_repo: IAuthRepository, time: Time):
        self.repo = attendance_repo
        self.auth_repo = auth_repo

    def save(self, user_id: int, lecture_id: int, course_id: int, student_id: int):
        is_course_professor = self.auth_repo.is_course_professor(user_id, course_id)
        is_course_student = self.auth_repo.is_course_student(user_id, lecture_id) and user_id == student_id
        if not is_course_professor and not is_course_student:
            raise NotAuthorizedException(
                "Couldn't save attendance. Only the student themself or the course professor is authorized to do so!")
        saved = self.repo.save(lecture_id, student_id)
        if not saved:
            raise NotFoundException(
                f"Couldn't save attendance. Lecture with ID: {lecture_id} in Course with ID: {course_id} doesn't exist")

    def delete(self, prof_id: int, lecture_id: int, course_id: int, student_id: int):
        is_course_professor = self.auth_repo.is_course_professor(prof_id, course_id)
        if not is_course_professor:
            raise NotAuthorizedException(
                "Couldn't delete attendance. Only the course professor is authorized to do so!")
        deleted = self.repo.delete(lecture_id, student_id)
        if not deleted:
            raise NotFoundException(
                f"Couldn't delete attendance. Attendance of student with ID: {student_id} in lecture with ID: {lecture_id} doesn't exist")

    def generate_qr_code_hash(self, lecture_id: int):
        time()
