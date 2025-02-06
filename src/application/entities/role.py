from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    PROFESSOR = "professor"
    STUDENT = "student"
