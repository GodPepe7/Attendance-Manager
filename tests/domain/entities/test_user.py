import pytest

from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import InvalidInputException


class TestUser:

    def test_user_factory_with_non_existing_role_raises(self):
        with pytest.raises(InvalidInputException) as exc:
            User.factory("alex", "alex@htw-berlin.de", "12345678", "janitor")

        assert str([role.value for role in Role]) and 'janitor' in str(exc.value)

    def test_user_factory_with_bad_email_input_raises(self):
        with pytest.raises(InvalidInputException) as exc:
            User.factory("alex", "not-an-email", "12345678", "student")

        assert "Invalid email" in str(exc.value)

    def test_user_factory_with_too_short_password_raises(self):
        with pytest.raises(InvalidInputException) as exc:
            User.factory("alex", "alex@htw-berlin.de", "1", "student")

        assert "atleast 8 characters long" in str(exc.value)

    def test_user_factory_hashes_password(self):
        password = "12345678"

        user = User.factory("alex", "alex@htw-berlin.de", password, "student")

        assert user.password_hash != password
        assert not user.check_password("4321")
        assert user.check_password(password)
