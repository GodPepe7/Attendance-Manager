import pytest

from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import InvalidCredentialsException, NotFoundException
from src.domain.services.user_service import UserService
from tests.conftest import setup_database, add_users


class TestUserService:
    @pytest.fixture
    def user_service(self, setup_database):
        session = setup_database
        repo = UserRepository(session())
        return session, UserService(repo)

    @pytest.fixture
    def user_service_with_users(self, add_users):
        session, _ = add_users
        repo = UserRepository(session())
        return session, UserService(repo)

    def test_get_all_users(self, user_service_with_users):
        session, user_service = user_service_with_users

        fetchedUsers = user_service.get_all()

        fetchedUsers.sort(key=lambda user: user.id)
        assert len(fetchedUsers) == 2
        assert fetchedUsers[0].id == 1 and fetchedUsers[0].name == "alex"
        assert fetchedUsers[1].id == 2 and fetchedUsers[1].name == "bob"

    def test_create_user(self, user_service_with_users):
        session, user_service = user_service_with_users
        test_user = User("deez", "deez@knees.com", "1234", Role.ADMIN, 3)

        user_service.create_user(test_user)

        fetched_user = session.get(User, 3)
        assert fetched_user
        assert fetched_user == test_user

    def test_get_by_id_of_existing_user(self, user_service_with_users):
        _, user_service = user_service_with_users

        fetched_user = user_service.get_by_id(1)

        assert fetched_user
        assert fetched_user.id == 1 and fetched_user.name == "alex"

    def test_get_by_id_of_non_existing_user(self, user_service_with_users):
        _, user_service = user_service_with_users

        with pytest.raises(NotFoundException) as exception:
            user_service.get_by_id(100)

        assert exception

    def test_authenticate_valid_credentials(self, user_service_with_users):
        _, user_service = user_service_with_users

        authenticated_user = user_service.authenticate("alex@abc.de", "1234")

        assert authenticated_user
        assert authenticated_user.id == 1 and authenticated_user.name == "alex"

    def test_authenticate_invalid_password(self, user_service_with_users):
        _, user_service = user_service_with_users

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("alex@abc.de", "ipwnedurpassword")

        assert exception

    def test_authenticate_invalid_email(self, user_service_with_users):
        _, user_service = user_service_with_users

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("hackerman@darkweb.xyz", "1234")

        assert exception

    def test_authenticate_invalid_email_and_password(self, user_service_with_users):
        _, user_service = user_service_with_users

        with pytest.raises(InvalidCredentialsException) as exception:
            user_service.authenticate("hackerman@darkweb.xyz", "superhackerman9000")

        assert exception
