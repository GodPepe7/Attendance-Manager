import re
from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from src.application.entities.role import Role
from src.application.exceptions import InvalidInputException


class InvalidRoleException(Exception):
    pass


@dataclass
class User:
    name: str
    email: str
    password_hash: str
    role: Role
    id: int = None

    def __repr__(self):
        return f"<User {self.id} {self.name}>"

    def __hash__(self):
        return hash((self.id, self.name))

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def factory(cls, name: str, email: str, password: str, role_input: str) -> "User":
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidInputException("Invalid email. A valid email looks like 'example@host.com'")

        try:
            role = Role(role_input)
        except ValueError:
            raise InvalidInputException(
                f"Invalid role \'{role_input}\'. Needs to be one of: {[role.value for role in Role]}")

        if len(password) < 8:
            raise InvalidInputException("Password too weak. Needs to be atleast 8 characters long")
        password_hash = generate_password_hash(password)

        return cls(name=name, email=email, password_hash=password_hash, role=role)
