from src.domain.dto import UserDto
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, InvalidInputException
from src.domain.ports.user_repository import IUserRepository
from src.domain.authorizer_utils import AuthorizerUtils


class AdminService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_all_professors(self, user: User) -> list[UserDto]:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        professors = self.user_repo.get_all_professors()
        return [prof.to_dto() for prof in professors]

    def delete_professor(self, user, professor_id: int) -> None:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        successfully_deleted = self.user_repo.delete_prof(professor_id)
        if not successfully_deleted:
            raise NotFoundException(f"Professor doesn't exist")

    def update_professor(self, user: User, user_dto: UserDto) -> None:
        AuthorizerUtils.check_if_role(user, Role.ADMIN)
        user = self.user_repo.get_by_email(user_dto.email)
        if user:
            raise InvalidInputException(f"Email '{user_dto.email}' is already in use. Choose another one")
        successfully_updated = self.user_repo.update_prof(user_dto)
        if not successfully_updated:
            raise NotFoundException(f"Professor doesn't exist")
