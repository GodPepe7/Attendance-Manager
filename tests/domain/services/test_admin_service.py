import random

import pytest

from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.dto import UserDto
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, UnauthorizedException
from src.domain.services.admin_service import AdminService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import users


class TestAdminService:
    @pytest.fixture
    def admin_service(self, db_session):
        self.users = [db_session.merge(user) for user in users]
        user_repo = UserRepository(db_session)
        admin_service = AdminService(user_repo)
        return db_session, admin_service

    @staticmethod
    def _assert_dto_equals_user(dto: UserDto, user: User):
        assert dto.id == user.id and dto.name == user.name and dto.email == user.email

    def test_get_all_professors_with_non_admin_raises(self, admin_service):
        _, admin_service = admin_service
        non_admin = User("foo", "foo@bar.de", "1234", random.choice([Role.PROFESSOR, Role.STUDENT]), 69420)

        with pytest.raises(UnauthorizedException) as exc:
            admin_service.get_all_professors(non_admin)

        assert "'Admin' can do this" in str(exc.value)

    def test_get_all_professors_only_returns_professors(self, admin_service):
        _, admin_service = admin_service
        expected_professors = [user for user in self.users if user.role == Role.PROFESSOR]
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        professors = admin_service.get_all_professors(test_admin)

        professors.sort(key=lambda prof: prof.id)
        assert len(professors) == len(expected_professors)
        for user_dto, user in zip(professors, expected_professors):
            self._assert_dto_equals_user(user_dto, user)

    def test_deleting_professor_with_non_admin_raises(self, admin_service):
        _, admin_service = admin_service
        non_admin = User("foo", "foo@bar.de", "1234", random.choice([Role.PROFESSOR, Role.STUDENT]), 69420)
        existing_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])

        with pytest.raises(UnauthorizedException) as exc:
            admin_service.delete_professor(non_admin, existing_professor)

        assert "'Admin' can do this" in str(exc.value)

    def test_deleting_existing_professor_works(self, admin_service):
        session, admin_service = admin_service
        existing_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        admin_service.delete_professor(test_admin, existing_professor.id)

        assert not session.get(User, existing_professor.id)

    def test_deleting_non_existing_professor_raises(self, admin_service):
        _, admin_service = admin_service
        non_existing_professor_id = 123456789
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        with pytest.raises(NotFoundException) as exc:
            admin_service.delete_professor(test_admin, non_existing_professor_id)

        assert "doesn't exist" in str(exc.value)
