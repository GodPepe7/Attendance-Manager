from abc import ABC, abstractmethod

from src.domain.entities.user import User


class IAttendanceRepository(ABC):
    @abstractmethod
    def save(self, lecture_id: int, student: User) -> bool:
        pass

    @abstractmethod
    def delete(self, lecture_id: int, student_id: int) -> bool:
        pass
