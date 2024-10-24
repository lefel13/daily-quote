# test_quotes.py
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
Test suite for the 'quotes' API endpoints in the 'daily_quote' project.

This test suite uses pytest and FastAPI's TestClient to simulate HTTP requests
and verify the correctness of the quote creation functionality in the API.
"""

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from ..quote_model import Quote


class TestQuotes:
    """
    A test class for the quote-related API endpoints.

    It contains test methods to verify the creation of quotes and ensure
    the database assigns unique primary keys.
    """

    def test_post(self, client: TestClient, session: Session):
        """
        Test creating a quote and verify that it is saved in the database.

        This test sends a POST request to create a new quote and checks
        whether the quote is stored correctly in the database.

        Args:
            client (TestClient): A FastAPI TestClient instance for sending HTTP requests.
            session (Session): A SQLModel session instance for database interaction.
        """
        author = "John Doe"
        text = "Hello World!"
        payload = {"author": author, "text": text}
        response = client.post("/quotes", json=payload)

        assert response.status_code == 200

        statement = select(Quote).where(
            Quote.author == author, Quote.text == text)
        results = session.exec(statement).fetchall()

        assert len(results) == 1

        quote_in_db = results[0]

        assert quote_in_db.author == author
        assert quote_in_db.text == text

    def test_post_response(self, client: TestClient):
        """
        Test the creation of a quote via the /quotes POST endpoint.

        This test verifies that when a valid quote is posted, the API responds
        with status code 200, and the returned JSON contains the correct quote
        data (author, text, and generated ID).

        Args:
            client (TestClient): A FastAPI TestClient instance for sending HTTP requests.
        """
        author = "John Doe"
        text = "Hello World!"
        payload = {"author": author, "text": text}
        response = client.post("/quotes", json=payload)

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["author"] == author
        assert response.json()["text"] == text

    def test_post_primary_key(self, client: TestClient):
        """
        Test that each posted quote receives a unique primary key.

        This test posts multiple quotes via the /quotes POST endpoint, and
        verifies that the ID of each created quote increments as expected.

        Args:
            client (TestClient): A FastAPI TestClient instance for sending HTTP requests.
        """
        payload = {"author": "John Doe", "text": "The first quote"}
        n = 10
        for i in range(1, n + 1):
            response = client.post("/quotes", json=payload)
        assert response.json()["id"] == n
