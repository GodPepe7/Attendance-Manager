from abc import ABC, abstractmethod


class IAuthRepository(ABC):
    @abstractmethod
    def is_course_professor(self, professor_id: int, course_id: int) -> bool:
        pass

    @abstractmethod
    def is_course_student(self, student_id: int, course_id: int) -> bool:
        pass
