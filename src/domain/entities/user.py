from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from src.domain.dto import UserDto
from src.domain.entities.role import Role, get_enum_by_value


class InvalidRoleException(Exception):
    pass


@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str
    role: Role

    def __repr__(self):
        return f"<User {self.id} {self.name}>"

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dto(self):
        return UserDto(id=self.id, name=self.name)


def user_factory(id: int, name: str, email: str, password: str, role_input: str) -> User:
    password_hash = generate_password_hash(password)
    role = get_enum_by_value(role_input)
    if not role:
        raise InvalidRoleException(f"Invalid role \'{role_input}\'.")
    return User(id, name, email, password_hash, role)
