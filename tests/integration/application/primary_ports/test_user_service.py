import random

import pytest

from src.adapters.secondary.user_repository_impl import UserRepository
from src.application.dto import UpdateUserRequestDto, UserResponseDto
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import InvalidCredentialsException, NotFoundException, UnauthorizedException, \
    DuplicateException
from src.application.primary_ports.user_service import UserService
from tests.fixtures import db_session
from tests.test_data import users


class TestUserService:
    @pytest.fixture
    def user_service(self, db_session):
        self.users = [db_session.merge(user) for user in users]
        repo = UserRepository(db_session)
        return db_session, UserService(repo)

    @staticmethod
    def _assert_dto_equals_user(dto: UpdateUserRequestDto | UserResponseDto, user: User):
        assert dto.id == user.id and dto.name == user.name and dto.email == user.email

    def test_create_user_persists_to_db(self, user_service):
        session, user_service = user_service
        test_user = User("deez", "deez@knees.com", "1234", Role.ADMIN, len(self.users) + 100)

        user_service.save(test_user)

        fetched_user = session.get(User, test_user.id)
        assert fetched_user
        assert fetched_user == test_user

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

    def test_get_all_professors_with_non_admin_raises(self, user_service):
        _, user_service = user_service
        non_admin = User("foo", "foo@bar.de", "1234", random.choice([Role.PROFESSOR, Role.STUDENT]), 69420)

        with pytest.raises(UnauthorizedException) as exc:
            user_service.get_all_professors(non_admin)

        assert "'admin' can do this" in str(exc.value)

    def test_get_all_professors_only_returns_professors(self, user_service):
        _, user_service = user_service
        expected_professors = [user for user in self.users if user.role == Role.PROFESSOR]
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        professors = user_service.get_all_professors(test_admin)

        professors.sort(key=lambda prof: prof.id)
        assert len(professors) == len(expected_professors)
        for user_dto, user in zip(professors, expected_professors):
            self._assert_dto_equals_user(user_dto, user)

    def test_deleting_professor_with_non_admin_raises(self, user_service):
        _, user_service = user_service
        non_admin = User("foo", "foo@bar.de", "1234", random.choice([Role.PROFESSOR, Role.STUDENT]), 69420)
        existing_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])

        with pytest.raises(UnauthorizedException) as exc:
            user_service.delete_professor(non_admin, existing_professor)

        assert "'admin' can do this" in str(exc.value)

    def test_deleting_existing_professor_works(self, user_service):
        session, user_service = user_service
        existing_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        user_service.delete_professor(test_admin, existing_professor.id)

        assert not session.get(User, existing_professor.id)

    def test_deleting_non_existing_professor_raises(self, user_service):
        _, user_service = user_service
        non_existing_professor_id = 123456789
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        with pytest.raises(NotFoundException) as exc:
            user_service.delete_professor(test_admin, non_existing_professor_id)

        assert "doesn't exist" in str(exc.value)

    def test_updating_with_non_admin_raises(self, user_service):
        _, user_service = user_service
        non_admin = User("foo", "foo@bar.de", "1234", random.choice([Role.PROFESSOR, Role.STUDENT]), 69420)
        random_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])
        update_professor_dto = UpdateUserRequestDto(random_professor.id, "Super Professor", "goat69@htw.de")

        with pytest.raises(UnauthorizedException) as exc:
            user_service.update_professor(non_admin, update_professor_dto)

        assert "'admin' can do this" in str(exc.value)

    def test_updating_existing_professor_persists_to_db(self, user_service):
        session, user_service = user_service
        existing_professor = random.choice([user for user in self.users if user.role == Role.PROFESSOR])
        update_professor_dto = UpdateUserRequestDto(existing_professor.id, "Super Professor", "goat69@htw.de")
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        user_service.update_professor(test_admin, update_professor_dto)

        fetched_professor = session.get(User, existing_professor.id)
        self._assert_dto_equals_user(update_professor_dto, fetched_professor)

    def test_update_existing_professor_with_already_used_email_raises(self, user_service):
        session, user_service = user_service
        professors = [user for user in self.users if user.role == Role.PROFESSOR]
        existing_professor = professors[0]
        existing_professor2 = professors[1]
        update_professor_dto = UpdateUserRequestDto(existing_professor.id, "Super Professor", existing_professor2.email)
        test_admin = User("admin", "admin@admin.de", "admin", Role.ADMIN, 69420)

        with pytest.raises(DuplicateException) as exc:
            user_service.update_professor(test_admin, update_professor_dto)

        assert exc
