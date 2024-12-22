from sqlalchemy.orm import scoped_session, sessionmaker, Session, registry, deferred, relationship
from sqlalchemy import create_engine, event, Table, Column, Integer, String, Enum, ForeignKey, Date

from src.adapters.flask.config.tables import metadata
from src.domain.entities.course import Course
from src.domain.entities.course_student import CourseStudent
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User


class DB:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri, echo=True)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))

        @event.listens_for(self.engine, "connect")
        def enable_sqlite_fks(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    def create_tables(self):
        metadata.create_all(self.engine)

    def get_db_session(self):
        return self.db_session

    def get_nested_db_session(self):
        connection = self.engine.connect()
        # begin the nested transaction
        transaction = connection.begin()
        # use the connection with the already started transaction
        nested_session = Session(bind=connection)
        yield transaction, nested_session
