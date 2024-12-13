from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
from src.domain.ports.user_repository import IUserRepository
from src.domain.services.authorizer_service import AuthorizerService


class AdminService:
    def __init__(self, user_repo: IUserRepository, authorizer: AuthorizerService):
        self.user_repo = user_repo
        self.authorizer = authorizer

    def get_all_professors(self, user: User) -> list[User]:
        self.authorizer.check_if_role(user, Role.ADMIN)
        return self.user_repo.get_all_professors()

    def delete_professor(self, user, professor_id: int) -> None:
        self.authorizer.check_if_role(user, Role.ADMIN)
        successfully_deleted = self.user_repo.delete(professor_id)
        if not successfully_deleted:
            raise NotFoundException(f"Professor with ID: {professor_id} doesn't exist")
