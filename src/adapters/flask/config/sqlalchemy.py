from flask import current_app
from sqlalchemy.orm import scoped_session, sessionmaker, registry, relationship, deferred, Session

from sqlalchemy import create_engine, Table, Column, Integer, String, Enum, ForeignKey, Date, event, MetaData
from src.domain.entities.course import Course
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User

db_session: scoped_session[Session]


def get_db_session():
    """
    Getter method to access the db_session
    This helps with import and provides a clean way to access the session
    """
    global db_session
    if db_session is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return db_session


def init_db(database_uri: str):
    global db_session
    engine = create_engine(database_uri, echo=False)
    db_session = scoped_session(sessionmaker(bind=engine))
    metadata = _init_db_structure()
    metadata.create_all(engine)

    # enforce foreign keys constraints on sqlite
    @event.listens_for(engine, "connect")
    def enable_sqlite_fks(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    @current_app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()


def _init_db_structure() -> MetaData:
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
        Column("course_id", Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False),
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
            "lectures": relationship("Lecture", cascade="all, delete, delete-orphan", collection_class=set),
            "enrolled_students": relationship("User", secondary=enrollment_table, collection_class=set)
        }
    )
    mapper_registry.map_imperatively(
        Lecture,
        lecture_table,
        properties={
            "attended_students": relationship("User", secondary=attendance_table, collection_class=set)
        }
    )
    return metadata
