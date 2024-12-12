import random

import pytest

from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
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

    def test_get_all_professors_only_returns_professors(self, admin_service):
        _, admin_service = admin_service
        expected_professors = [user for user in self.users if user.role == Role.PROFESSOR]

        professors = admin_service.get_all_professors()

        assert len(professors) == len(expected_professors)
        assert len(set(professors).intersection(expected_professors)) == len(expected_professors)

    def test_deleting_existing_professor_works(self, admin_service):
        session, admin_service = admin_service
        random_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])

        admin_service.delete_professor(random_professor.id)

        assert not session.get(User, random_professor.id)

    def test_deleting_non_existing_professor_raises(self, admin_service):
        _, admin_service = admin_service
        non_existing_professor_id = 123456789

        with pytest.raises(NotFoundException) as exc:
            admin_service.delete_professor(non_existing_professor_id)

        assert "doesn't exist" in str(exc.value)
