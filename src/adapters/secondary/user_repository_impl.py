from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.application.dto import UpdateUserRequestDto
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import NotFoundException
from src.application.secondary_ports.user_repository import IUserRepository


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

    def save(self, user: User) -> int:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user.id

    def delete_prof(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user or user.role != Role.PROFESSOR:
            raise NotFoundException(f"Professor with ID {user_id} doesn't exist")
        self.session.delete(user)
        self.session.commit()
        return True

    def update_prof(self, user_dto: UpdateUserRequestDto) -> None:
        user = self.session.get(User, user_dto.id)
        if not user or user.role != Role.PROFESSOR:
            raise NotFoundException(f"Professor with ID {user_dto.id} doesn't exist")
        user.name = user_dto.name
        user.email = user_dto.email
        try:
            self.session.commit()
        except IntegrityError:
            raise NotFoundException(f"Email {UpdateUserRequestDto.email} already in use by other user")
