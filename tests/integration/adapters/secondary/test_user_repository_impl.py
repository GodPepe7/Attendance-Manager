import random

import pytest

from src.adapters.secondary.user_repository_impl import UserRepository
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import DuplicateException
from tests.fixtures import db_session
from tests.test_data import users
from unittest.mock import Mock


class TestCourseStudentRepository:

    @pytest.fixture
    def user_repo(self, db_session):
        self.users = [db_session.merge(user) for user in users]
        return UserRepository(db_session)

    @pytest.fixture
    def user_repo_mock(self):
        mock_repo = Mock(UserRepository)

    def test_update_to_email_that_is_already_used_raises(self, user_repo):
        existing_professors = [user for user in self.users if user.role == Role.PROFESSOR]
        prof1 = existing_professors[0]
        prof2 = existing_professors[1]

        prof1.email = prof2.email
        with pytest.raises(DuplicateException) as exc:
            user_repo.update(prof1)

        assert exc

    def test_save_with_email_that_is_already_used_raises(self, user_repo):
        existing_user = random.choice(self.users)
        new_user = User("hero", existing_user.email, "", Role.STUDENT)

        with pytest.raises(DuplicateException) as exc:
            user_repo.save(new_user)

        assert exc
