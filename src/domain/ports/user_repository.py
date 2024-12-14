from abc import ABC, abstractmethod
from typing import Optional

from src.domain.dto import UserDto
from src.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[User]:
        pass

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
    def save(self, entity: User) -> None:
        pass

    @abstractmethod
    def delete_prof(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def update_prof(self, user_dto: UserDto) -> bool:
        pass
