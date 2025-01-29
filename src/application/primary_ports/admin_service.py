from src.application.dto import UserResponseDto, UpdateUserRequestDto
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import NotFoundException, InvalidInputException
from src.application.secondary_ports.user_repository import IUserRepository
from src.application.authorizer_utils import AuthorizerUtils


class AdminService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_all_professors(self, user: User) -> list[UserResponseDto]:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        professors = self.user_repo.get_all_professors()
        return [prof.to_dto() for prof in professors]

    def delete_professor(self, user, professor_id: int) -> None:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        self.user_repo.delete_prof(professor_id)

    def update_professor(self, user: User, user_dto: UpdateUserRequestDto) -> None:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        user = self.user_repo.get_by_email(user_dto.email)
        if user:
            raise InvalidInputException(f"Email '{user_dto.email}' is already in use. Choose another one")
        self.user_repo.update_prof(user_dto)
