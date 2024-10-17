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
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine


class QuoteBase(SQLModel):
    author: str
    text: str


class Quote(QuoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class QuoteRequest(QuoteBase):
    pass


class QuoteResponse(QuoteBase):
    id: int


# Database file and connection URL for SQLite.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# "check_same_thread" is set to False to make sure we don't share the
# same session in more than one request and we also need to disable it
# because in FastAPI each request could be handled by multiple interacting
# threads.
connect_args = {"check_same_thread": False}
# Create the database engine, which will handle connections to the SQLite
# database. The echo=True parameter is for logging SQL statements, useful
# for debugging.
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        # Use yield instead of return to go back here and close the 'with'
        # block, and cleanup and close the session
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# FastAPI instance to define and serve the REST API.
app = FastAPI(lifespan=lifespan)


@app.post("/quotes/", response_model=QuoteResponse)
async def create_quote(
        *, session: Session = Depends(get_session), quote: QuoteRequest):
    # Get a database model from the model passed within the request
    quote_in_db = Quote.model_validate(quote)
    # Add it in a transaction to the database
    session.add(quote_in_db)
    # Commit the transaction
    session.commit()
    # Refresh the quote object to include its generated ID
    session.refresh(quote_in_db)
    # Return the newly created quote, compliant with the response model
    return quote_in_db
