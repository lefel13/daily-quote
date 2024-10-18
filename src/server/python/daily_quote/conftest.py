# conftest.py
#
# Copyright (C) 2024 Felix GAIDON
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
This module defines pytest fixtures for setting up a test environment in the
'daily_quote' project.

It includes fixtures for creating a session to an in-memory SQLite database
and for creating a test client for FastAPI routes.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from .main import app
from .database import get_session


@pytest.fixture(name="session")
def session_fixture():
    """
    Pytest fixture to provide a session for tests using an in-memory SQLite database.

    This fixture sets up the database with an in-memory SQLite engine, which is
    useful for testing purposes because it avoids writing to a real database file.
    It also ensures that the database schema is created before tests are run.

    Yields:
        Session: A SQLModel session for interacting with the test database.
    """
    engine = create_engine(
        "sqlite://",  # In-memory SQLite database.
        connect_args={"check_same_thread": False},
        # For compatibility with multi-threading in FastAPI.
        poolclass=StaticPool  # Use StaticPool to keep the database in memory.
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Pytest fixture to provide a test client for FastAPI routes.

    This fixture overrides the default database session with a test session,
    allowing tests to run against the in-memory database set up by the
    'session_fixture'. It also ensures that the dependency override is cleared
    after the tests.

    Args:
        session (Session): The in-memory database session.

    Yields:
        TestClient: A FastAPI test client for making requests to the API.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
