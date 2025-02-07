from abc import ABC, abstractmethod
from typing import Optional

from src.application.dto import UpdateUserRequestDto
from src.application.entities.user import User


class IUserRepository(ABC):
    
    @abstractmethod
    def get_all_professors(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, entity: User) -> int:
        pass

    @abstractmethod
    def delete(self, professor: User) -> None:
        pass

    @abstractmethod
    def update(self, prof_dto: UpdateUserRequestDto) -> None:
        pass
