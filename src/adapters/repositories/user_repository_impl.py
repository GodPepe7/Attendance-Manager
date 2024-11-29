from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.domain.ports.user_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.session.scalars(stmt).all())

    def get_by_id(self, id: int) -> Optional[User]:
        return self.session.get(User, id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalars(stmt).first()

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()
