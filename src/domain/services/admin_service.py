from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
from src.domain.ports.user_repository import IUserRepository


class AdminService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_all_professors(self) -> list[User]:
        return self.user_repo.get_all_professors()

    def delete_professor(self, professor_id: int) -> None:
        successfully_deleted = self.user_repo.delete(professor_id)
        if not successfully_deleted:
            raise NotFoundException(f"Professor with ID: {professor_id} doesn't exist")
