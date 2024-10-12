# main.py
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

from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine


class Quote(SQLModel, table=True):
    """
    A model representing a quote with an author and text.

    Attributes:
        id (Optional[int]): The unique identifier of the quote (auto-incremented).
        author (str): The author of the quote.
        text (str): The content of the quote.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    text: str


# Database file and connection URL for SQLite.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Create the database engine, which will handle connections to the SQLite database.
# The echo=True parameter is for logging SQL statements, useful for debugging.
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    """
    Create the database and its tables based on the defined models.

    This function uses SQLModel's metadata to create all tables
    defined by model classes inheriting from SQLModel, such as the Quote model.
    """
    SQLModel.metadata.create_all(engine)


# FastAPI instance to define and serve the REST API.
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the lifespan of the FastAPI application.

    This function ensures that the database and its tables are created
    when the application starts, and yields control back to the main event loop.
    """
    create_db_and_tables()
    yield


@app.post("/quotes/")
async def create_quote(quote: Quote):
    """
    Create a new quote in the database.

    This endpoint allows users to submit a new quote by providing the author's
    name and the quote's content. The quote is saved in the database, and the
    newly created quote object is returned.

    Args:
        quote (Quote): A Quote object containing the author's name and the quote's content.

    Returns:
        Quote: The newly created Quote object with its generated ID.
    """
    # Create a session with the database, add the quote, and commit the
    # transaction.
    with Session(engine) as session:
        session.add(quote)
        session.commit()
        # Refresh the quote object to include its generated ID.
        session.refresh(quote)

    # Return the newly created quote.
    return quote
