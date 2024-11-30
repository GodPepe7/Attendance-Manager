from abc import ABC, abstractmethod


class IAttendanceRepository(ABC):
    @abstractmethod
    def save(self, lecture_id: int, student_id: int) -> bool:
        pass

    @abstractmethod
    def delete(self, lecture_id: int, student_id: int) -> bool:
        pass
