from typing import Optional

from src.application.entities.user import User
from src.application.exceptions import InvalidCredentialsException, NotFoundException, InvalidInputException
from src.application.secondary_ports.user_repository import IUserRepository


class UserService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def create_user(self, user: User):
        self.repo.save(user)

    def get_all(self) -> list[User]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[User]:
        user = self.repo.get_by_id(id)
        if not user:
            raise NotFoundException(f"User with ID: {id} doesn't exist")
        return user

    def authenticate(self, email: str, password: str) -> User:
        """
        Checks if the passed in credentials are correct and returns the User if so.
        Otherwise, raises an InvalidCredentialsException.
        """

        user = self.repo.get_by_email(email)
        if user and user.check_password(password):
            return user
        else:
            raise InvalidCredentialsException()
