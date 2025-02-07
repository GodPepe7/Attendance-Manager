from typing import Optional

from src.application.authorizer_utils import AuthorizerUtils
from src.application.dto import UserResponseDto, UpdateUserRequestDto
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import InvalidCredentialsException, NotFoundException, InvalidInputException
from src.application.secondary_ports.user_repository import IUserRepository


class UserService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def save(self, user: User):
        self.repo.save(user)

    def get_by_id(self, id: int) -> Optional[User]:
        user = self.repo.get_by_id(id)
        if not user:
            raise NotFoundException(f"User with ID: {id} doesn't exist")
        return user

    def get_all_professors(self, user: User) -> list[UserResponseDto]:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        professors = self.repo.get_all_professors()
        return [UserResponseDto(prof.id, prof.name, prof.email) for prof in professors]

    def delete_professor(self, user, professor_id: int) -> None:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        professor = self.repo.get_by_id(professor_id)
        if not professor or professor.role != Role.PROFESSOR:
            raise NotFoundException(f"Professor with ID {professor_id} doesn't exist")
        self.repo.delete(professor)

    def update_professor(self, user: User, user_dto: UpdateUserRequestDto) -> None:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        user = self.repo.get_by_email(user_dto.email)
        if user and user.id != user_dto.id:
            raise InvalidInputException(f"Email '{user_dto.email}' is already in use.")
        self.repo.update(user_dto)

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
