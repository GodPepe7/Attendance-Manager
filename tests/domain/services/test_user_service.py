import random

import pytest

from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import InvalidCredentialsException, NotFoundException
from src.domain.services.user_service import UserService
from tests.conftest import engine, tables, add_data, db_session
from tests.test_data import users


class TestUserService:
    @pytest.fixture
    def user_service(self, db_session):
        self.users = [db_session.merge(user) for user in users]
        repo = UserRepository(db_session)
        return db_session, UserService(repo)

    def test_create_user(self, user_service):
        session, user_service = user_service
        test_user = User("deez", "deez@knees.com", "1234", Role.ADMIN, 4)

        user_service.create_user(test_user)

        fetched_user = session.get(User, 4)
        assert fetched_user
        assert fetched_user == test_user

    def test_get_all_users(self, user_service):
        session, user_service = user_service

        fetchedUsers = user_service.get_all()

        fetchedUsers.sort(key=lambda user: user.id)
        assert len(fetchedUsers) == 3
        assert fetchedUsers[0].id == self.users[0].id and fetchedUsers[0].name == self.users[0].name
        assert fetchedUsers[1].id == self.users[1].id and fetchedUsers[1].name == self.users[1].name

    def test_get_by_id_of_existing_user(self, user_service):
        _, user_service = user_service
        existing_user = random.choice(self.users)

        fetched_user = user_service.get_by_id(existing_user.id)

        assert fetched_user
        assert fetched_user.id == existing_user.id and fetched_user.name == existing_user.name

    def test_get_by_id_of_non_existing_user(self, user_service):
        _, user_service = user_service

        with pytest.raises(NotFoundException) as exception:
            user_service.get_by_id(100)

        assert exception

    def test_authenticate_valid_credentials(self, user_service):
        _, user_service = user_service
        existing_user = random.choice(self.users)

        authenticated_user = user_service.authenticate(existing_user.email, "1234")

        assert authenticated_user
        assert authenticated_user.id == existing_user.id and authenticated_user.name == existing_user.name

    def test_authenticate_invalid_password(self, user_service):
        _, user_service = user_service

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("alex@abc.de", "ipwnedurpassword")

        assert exception

    def test_authenticate_invalid_email(self, user_service):
        _, user_service = user_service

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("hackerman@darkweb.xyz", "1234")

        assert exception

    def test_authenticate_invalid_email_and_password(self, user_service):
        _, user_service = user_service

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("hackerman@darkweb.xyz", "superhackerman9000")

        assert exception
