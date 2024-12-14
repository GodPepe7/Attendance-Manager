from sqlalchemy.orm import scoped_session, sessionmaker, registry, relationship, deferred, Session

from sqlalchemy import create_engine, Table, Column, Integer, String, Enum, ForeignKey, Date, event
from src.domain.entities.course import Course
from src.domain.entities.enrollment import Enrollment
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User

db_session: scoped_session[Session]


def get_db_session():
    global db_session
    if db_session is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return db_session


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
    Column("name", String(50), nullable=False),
    Column("professor_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
)
lecture_table = Table(
    "lecture",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("course_id", Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False),
    Column("date", Date, nullable=False)
)
enrollment_table = Table(
    "enrollment",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("student_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("course_id", Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
)
attendance_table = Table(
    "attendance",
    metadata,
    Column("enrollment_id", Integer, ForeignKey("enrollment.id", ondelete="CASCADE"), primary_key=True,
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
        "enrolled_students": relationship("Enrollment", cascade="all, delete",
                                          collection_class=set)
    }
)
mapper_registry.map_imperatively(
    Enrollment,
    enrollment_table,
    properties={
        "student": relationship("User"),
        "attended_lectures": relationship("Lecture", backref="lecture",
                                          secondary=attendance_table, cascade="all, delete", passive_deletes=True,
                                          collection_class=set)
    }
)


def init_db(database_uri: str):
    global db_session
    engine = create_engine(database_uri, echo=False)
    db_session = scoped_session(sessionmaker(bind=engine))
    metadata.create_all(engine)

    # enforce foreign keys constraints on sqlite
    @event.listens_for(engine, "connect")
    def enable_sqlite_fks(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
