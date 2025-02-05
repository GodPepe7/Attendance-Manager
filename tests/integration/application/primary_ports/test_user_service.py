import random

import pytest

from src.adapters.secondary.user_repository_impl import UserRepository
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import InvalidCredentialsException, NotFoundException
from src.application.primary_ports.user_service import UserService
from tests.fixtures import engine, tables, add_data, db_session
from tests.test_data import users


class TestUserService:
    @pytest.fixture
    def user_service(self, db_session):
        self.users = [db_session.merge(user) for user in users]
        repo = UserRepository(db_session)
        return db_session, UserService(repo)

    def test_create_user_persists_to_db(self, user_service):
        session, user_service = user_service
        test_user = User("deez", "deez@knees.com", "1234", Role.ADMIN, len(self.users) + 100)

        user_service.create_user(test_user)

        fetched_user = session.get(User, test_user.id)
        assert fetched_user
        assert fetched_user == test_user

    def test_get_all_users_returns_all_users(self, user_service):
        session, user_service = user_service

        fetchedUsers = user_service.get_all()

        fetchedUsers.sort(key=lambda user: user.id)
        assert len(fetchedUsers) == len(self.users)
        assert len(set(fetchedUsers).intersection(self.users)) == len(self.users)

    def test_get_by_id_of_existing_user_returns_user(self, user_service):
        _, user_service = user_service
        existing_user = random.choice(self.users)

        fetched_user = user_service.get_by_id(existing_user.id)

        assert fetched_user
        assert fetched_user.id == existing_user.id and fetched_user.name == existing_user.name

    def test_get_by_id_of_non_existing_user_raises(self, user_service):
        _, user_service = user_service

        with pytest.raises(NotFoundException) as exception:
            user_service.get_by_id(len(self.users) + 100)

        assert exception

    def test_authenticate_with_valid_credentials_returns_user(self, user_service):
        _, user_service = user_service
        existing_user = random.choice(self.users)

        authenticated_user = user_service.authenticate(existing_user.email, "1234")

        assert authenticated_user
        assert authenticated_user.id == existing_user.id and authenticated_user.name == existing_user.name

    def test_authenticate_with_invalid_password_raises(self, user_service):
        _, user_service = user_service
        existing_user = random.choice(self.users)

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate(existing_user.email, "ipwnedurpassword")

        assert exception

    def test_authenticate_with_invalid_email_raises(self, user_service):
        _, user_service = user_service

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("hackerman@darkweb.xyz", "1234")

        assert exception

    def test_authenticate_with_invalid_email_and_password_raises(self, user_service):
        _, user_service = user_service

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("hackerman@darkweb.xyz", "superhackerman9000")

        assert exception
