from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.application.dto import UpdateUserRequestDto
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import NotFoundException, DuplicateException
from src.application.secondary_ports.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

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
        try:
            self.session.commit()
        except IntegrityError:
            raise DuplicateException(f"Email already in use by other")
        self.session.refresh(user)
        return user.id

    def delete(self, user: User) -> bool:
        self.session.delete(user)
        self.session.commit()
        return True

    def update(self, user: User) -> None:
        try:
            self.session.commit()
        except IntegrityError:
            raise DuplicateException(f"Email already in use by other")
