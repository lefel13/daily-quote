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
import os
from .main import app, sqlite_file_name, create_db_and_tables
from fastapi.testclient import TestClient

# Create a TestClient for the FastAPI app
client = TestClient(app)


def clear_db():
    """
    Ensure that the database.db file is deleted before each test,
    clearing all data.

    This function is useful for tests that require a clean state
    by removing the existing SQLite database file if it exists.
    """
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)


@pytest.fixture(autouse=True)
def pre_and_post_conditions():
    """
    This pytest fixture sets up pre-conditions and post-conditions
    for each test.

    It ensures that the database is cleared and recreated before
    each test by calling `clear_db()` and `create_db_and_tables()`.
    """
    # Pre conditions: Clear the database and recreate the schema
    clear_db()
    create_db_and_tables()
    yield
    # Post conditions: Any cleanup code can go here if needed


class TestQuotes:
    """
    A test class for testing the /quotes endpoint in the FastAPI app.

    Contains tests to ensure that quotes can be posted and that
    the primary key increments correctly.
    """

    def test_post(self, pre_and_post_conditions):
        """
        Test the POST /quotes endpoint.

        This test checks that a quote can be posted with a valid
        author and text, and the response contains the expected
        data including an auto-generated ID.
        """
        author = "John Doe"
        text = "Hello World!"
        payload = {"author": author, "text": text}
        response = client.post("/quotes", json=payload)
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["author"] == author
        assert response.json()["text"] == text

    def test_post_primary_key(self, pre_and_post_conditions):
        """
        Test that the primary key (id) increments correctly.

        This test posts the same quote multiple times to the /quotes
        endpoint and checks that the `id` field increments for each
        new entry, reaching the expected value for the last entry.
        """
        payload = {"author": "John Doe", "text": "The first quote"}
        n = 10
        for i in range(1, n + 1):
            response = client.post("/quotes", json=payload)
        assert response.json()["id"] == n
