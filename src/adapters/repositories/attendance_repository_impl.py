from sqlalchemy.orm import Session

from src.domain.entities.enrollment import Enrollment
from src.domain.entities.lecture import Lecture
from src.domain.ports.attendance_repository import IAttendanceRepository


class AttendanceRepository(IAttendanceRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, lecture_id: int, enrollment_id: int) -> bool:
        lecture = self.session.get(Lecture, lecture_id)
        enrollment = self.session.get(Enrollment, enrollment_id)
        if not enrollment or not lecture or not enrollment.course_id == lecture.course_id:
            return False
        lecture.attended_students.add(enrollment)
        self.session.commit()
        return True

    def delete(self, lecture_id: int, enrollment_id: int) -> bool:
        attended_student = self.session.get(Enrollment, enrollment_id)
        lecture = self.session.get(Lecture, lecture_id)
        if not attended_student or not lecture:
            return False
        try:
            lecture.attended_students.remove(attended_student)
            self.session.commit()
            return True
        except KeyError:
            return False
