from src.domain.entities.user import User
from src.domain.exceptions import InvalidCredentialsException
from src.domain.ports.user_repository import IUserRepository


class UserService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def create_user(self, user: User):
        self.repo.save(user)

    def get_all(self) -> list[User]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> User:
        return self.repo.get_by_id(id)

    def authenticate(self, email: str, password: str) -> User:
        """Checks if the passed in credentials are correct and returns the User if so. Otherwise, raises an InvalidCredentialsException"""
        user = self.repo.get_by_email(email)
        if user and user.check_password(password):
            return user
        else:
            raise InvalidCredentialsException()
