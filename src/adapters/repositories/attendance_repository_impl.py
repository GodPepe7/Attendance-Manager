import logging

from sqlalchemy.orm import Session

from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User
from src.domain.ports.attendance_repository import IAttendanceRepository


class AttendanceRepository(IAttendanceRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, lecture_id: int, student_id: int) -> bool:
        student = self.session.get(User, student_id)
        lecture = self.session.get(Lecture, lecture_id)
        if not student or not lecture:
            return False
        lecture.attended_students.add(student)
        return True

    def delete(self, lecture_id: int, student_id: int) -> bool:
        student = self.session.get(User, student_id)
        lecture = self.session.get(Lecture, lecture_id)
        if not student or not lecture:
            return False
        try:
            lecture.attended_students.remove(student)
            self.session.delete()
            return True
        except Exception:
            logging.error("couldn't find student in set")
            return False
