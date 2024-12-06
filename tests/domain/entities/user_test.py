import pytest

from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import InvalidInputException


def test_user_factory_validates_role_input():
    with pytest.raises(InvalidInputException) as exception:
        User.factory("alex", "alex@htw-berlin.de", "1234", "janitor")

    assert str([role.value for role in Role]) and 'janitor' in str(exception.value)


def test_user_factory_hashes_password():
    password = "1234"

    user = User.factory("alex", "alex@htw-berlin.de", password, "student")

    assert user.password_hash != password
    assert not user.check_password("4321")
    assert user.check_password(password)
