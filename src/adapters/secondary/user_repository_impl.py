from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from src.domain.dto import UserResponseDto
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.ports.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.session.scalars(stmt).all())

    def get_all_professors(self) -> list[User]:
        stmt = select(User).where(User.role == Role.PROFESSOR)
        return list(self.session.scalars(stmt).all())

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)

    def get_students_by_name_starting_with(self, name_prefix: str) -> list[User]:
        stmt = select(User).where(User.name.startswith(name_prefix), User.role == Role.STUDENT)
        return list(self.session.scalars(stmt).all())

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def delete_prof(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user or user.role != Role.PROFESSOR:
            return False
        self.session.delete(user)
        self.session.commit()
        return True

    def update_prof(self, user_dto: UserResponseDto) -> bool:
        user = self.session.get(User, user_dto.id)
        if not user or user.role != Role.PROFESSOR:
            return False
        user.name = user_dto.name
        user.email = user_dto.email
        self.session.commit()
        return True
