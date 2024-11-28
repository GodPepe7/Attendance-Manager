from sqlalchemy import create_engine, Table, Column, Integer, String, Enum, ForeignKey, DATETIME, Date
from sqlalchemy.orm import scoped_session, sessionmaker, registry, relationship, deferred

from src.domain.entities.course import Course
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User


engine = create_engine('sqlite:///dev.db', echo=True)

def init_db():
    mapper_registry = registry()
    metadata = mapper_registry.metadata

    user_table = Table(
        "user",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(50), nullable=False),
        Column("email", String(30), nullable=False, unique=True),
        Column("password_hash", String(100), nullable=False),
        Column("role", Enum(Role), nullable=False)
    )
    course_table = Table(
        "course",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(50), nullable=False),
        Column("professor_id", Integer, ForeignKey("user.id"), nullable=False)
    )
    enrollment_table = Table(
        "enrollment",
        metadata,
        Column("student_id", Integer, ForeignKey("user.id"), primary_key=True, nullable=False),
        Column("course_id", Integer, ForeignKey("course.id"), primary_key=True, nullable=False)
    )
    lecture_table = Table(
        "lecture",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("course_id", Integer, ForeignKey("course.id"), nullable=False),
        Column("date", Date, nullable=False)
    )
    attendance_table = Table(
        "attendance",
        metadata,
        Column("student_id", Integer, ForeignKey("user.id"), primary_key=True, nullable=False),
        Column("lecture_id", Integer, ForeignKey("lecture.id"), primary_key=True, nullable=False)
    )

    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "password_hash": deferred(user_table.c.password_hash)
        }
    )
    mapper_registry.map_imperatively(
        Course,
        course_table,
        properties={
            "professor": relationship("User", lazy="select"),
            "lectures": relationship("Lecture"),
            "enrolled_students": relationship("User", secondary=enrollment_table)
        }
    )
    mapper_registry.map_imperatively(
        Lecture,
        lecture_table,
        properties={
            "attended_students": relationship("User", secondary=attendance_table)
        }
    )
    metadata.create_all(engine)



db_session = scoped_session(sessionmaker(bind=engine))
