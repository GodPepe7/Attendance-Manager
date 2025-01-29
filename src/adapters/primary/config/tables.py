from sqlalchemy import Table, Column, Integer, String, Enum, ForeignKey, Date, DateTime
from sqlalchemy.orm import registry, deferred, relationship

from src.application.entities.course import Course
from src.application.entities.course_student import CourseStudent
from src.application.entities.lecture import Lecture
from src.application.entities.role import Role
from src.application.entities.user import User

mapper_registry = registry()
metadata = mapper_registry.metadata

user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("email", String(30), nullable=False, unique=True, index=True),
    Column("password_hash", String(100), nullable=False),
    Column("role", Enum(Role), nullable=False)
)
course_table = Table(
    "course",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False, unique=True, index=True),
    Column("professor_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("password_hash", String(100)),
    Column("password_expiration_datetime", DateTime)
)
lecture_table = Table(
    "lecture",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("course_id", Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False),
    Column("date", Date, nullable=False)
)
course_student_table = Table(
    "course_student",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("student_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("course_id", Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
)
attendance_table = Table(
    "attendance",
    metadata,
    Column("course_student_id", Integer, ForeignKey("course_student.id", ondelete="CASCADE"), primary_key=True,
           nullable=False),
    Column("lecture_id", Integer, ForeignKey("lecture.id", ondelete="CASCADE"), primary_key=True, nullable=False)
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "password_hash": deferred(user_table.c.password_hash)
    }
)
mapper_registry.map_imperatively(Lecture, lecture_table)
mapper_registry.map_imperatively(
    Course,
    course_table,
    properties={
        "professor": relationship("User"),
        "lectures": relationship("Lecture", cascade="all, delete",
                                 collection_class=set),
        "students": relationship("CourseStudent", cascade="all, delete",
                                 collection_class=set)
    }
)
mapper_registry.map_imperatively(
    CourseStudent,
    course_student_table,
    properties={
        "student": relationship("User"),
        "attended_lectures": relationship("Lecture", backref="lecture",
                                          secondary=attendance_table, cascade="all, delete", passive_deletes=True,
                                          collection_class=set)
    }
)
