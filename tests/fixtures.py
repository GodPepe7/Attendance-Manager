import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.adapters.primary.config.tables import metadata
from tests.test_data import courses


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

    return engine


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
