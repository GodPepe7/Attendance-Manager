from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, event

from src.adapters.primary.config.tables import metadata


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
