import contextlib
from datetime import datetime, timedelta
from threading import Thread

import pytest
from dependency_injector import providers, containers
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.adapters.primary.app import create_app
from src.adapters.primary.config.db import DB
from src.adapters.primary.config.tables import metadata
from src.application.secondary_ports.clock import IClock
from tests.test_data import courses
from tests.test_data_e2e import courses as e2e_courses, course_expiration_datetime


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope="session")
def add_data(tables, engine):
    session = Session(bind=engine, expire_on_commit=False)

    session.add_all(courses)
    session.commit()
    session.close()

    yield engine


@pytest.fixture
def db_session(add_data):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    engine = add_data
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


class TestClock(IClock):
    def __init__(self, fixed_datetime: datetime):
        self.current = fixed_datetime

    def get_current_datetime(self) -> datetime:
        pass


class FixedClock(IClock):
    def __init__(self, fixed_datetime: datetime):
        self.current = fixed_datetime

    def get_current_datetime(self) -> datetime:
        return self.current


class TestOverrideContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict({
        "fernet_key": "test"
    })
    db = providers.Singleton(DB, db_uri="sqlite:///test2.db")
    db_session = providers.Factory(db.provided.get_db_session())
    fixed_datetime = course_expiration_datetime - timedelta(hours=1)
    clock = providers.Factory(
        FixedClock, fixed_datetime=fixed_datetime
    )


@pytest.fixture(scope="module")
def start_test_app():
    app = create_app(config_path="config/test_config.py")
    testContainer = TestOverrideContainer()
    app.container.override(testContainer)

    db = app.container.db()
    db.create_tables()
    session = db.get_db_session()
    session.add_all(e2e_courses)
    session.commit()

    def run_app():
        app.run(host="127.0.0.1", port=5000)

    thread = Thread(target=run_app, daemon=True)
    thread.start()

    yield app

    with contextlib.closing(db.engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()
