import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.adapters.flask.config.sqlalchemy import init_db, get_db_session, metadata
from src.domain.entities.course import Course
from src.domain.entities.user import User


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture
def db_session_no_data(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
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


@pytest.fixture
def db_session_with_data(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    session = Session(bind=engine)
    from tests.test_data import courses
    session.add_all(courses)
    session.commit()

    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    nested_session = Session(bind=connection)

    yield nested_session

    nested_session.close()
    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture
def add_users(dbsession):
    session = dbsession
    from tests.test_data import users
    session.add_all(users)
    session.commit()

    yield session


@pytest.fixture
def add_test_data(add_users):
    session = add_users
    from tests.test_data import courses
    session.add_all(courses)
    session.commit()

    yield session
