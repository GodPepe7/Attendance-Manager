from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    PROFESSOR = "professor"
    STUDENT = "student"


role_dict = {i.value: i.name for i in Role}


def get_enum_by_value(value: str):
    return role_dict.get(value)
