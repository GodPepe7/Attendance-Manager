from sqlalchemy.orm import Session

from src.domain.entities.enrollment import Enrollment
from src.domain.entities.lecture import Lecture
from src.domain.ports.attendance_repository import IAttendanceRepository


class AttendanceRepository(IAttendanceRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, lecture_id: int, enrollment_id: int) -> bool:
        attended_student = self.session.get(Enrollment, enrollment_id)
        lecture = self.session.get(Lecture, lecture_id)
        if not attended_student or not lecture:
            return False
        lecture.attended_students.add(attended_student)
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
