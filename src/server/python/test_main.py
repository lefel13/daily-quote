# test_main.py
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

import pytest
from .main import app, get_session
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture(name="session")
def session_fixture():
    # poolclass set to StaticPool to use an in-memory database
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestQuotes:
    def test_post_response(self, client: TestClient):
        author = "John Doe"
        text = "Hello World!"
        payload = {"author": author, "text": text}
        response = client.post("/quotes", json=payload)
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["author"] == author
        assert response.json()["text"] == text

    def test_post_primary_key(self, client: TestClient):
        payload = {"author": "John Doe", "text": "The first quote"}
        n = 10
        for i in range(1, n + 1):
            response = client.post("/quotes", json=payload)
        assert response.json()["id"] == n
