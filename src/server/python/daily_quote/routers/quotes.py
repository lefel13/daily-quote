# quotes.py
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
This module defines the API routes for handling quotes in the 'daily_quote' project.

It includes a route to create a new quote using FastAPI and SQLModel, and stores the
quote in the SQLite database.
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..quote_model import Quote, QuoteRequest, QuoteResponse
from ..database import get_session

# Define the router for handling quote-related operations.
router = APIRouter(prefix="/quotes", tags=["quotes"])


# We want to allow clients to set different offset and limit values than
# the default ones (0 for offset and 10 for limit). But we don't want them
# to be able to set a limit of something like 9999, that's over 9000! So,
# to prevent it, we add additional validation to the limit query
# parameter, declaring that it has to be less than or equal to 100 with
# le=100.
@router.get("/", response_model=List[QuoteResponse])
async def read_quotes(*, session: Session = Depends(get_session),
                      offset: int = 0, limit: int = Query(default=10, le=100)):
    """
    Retrieve a list of quotes from the database with pagination.

    This endpoint fetches quotes, allowing clients to specify an offset
    and limit for pagination. It limits the maximum number of results
    to 100 to prevent excessive data retrieval.

    Args:
        session (Session): The database session for interacting with the database.
        offset (int): The number of items to skip in the result set.
        limit (int): The maximum number of items to return (default is 10, maximum is 100).

    Returns:
        List[QuoteResponse]: A list of quotes, each containing an author, text, and ID.
    """
    quotes = session.exec(
        select(Quote).offset(offset).limit(limit)).all()
    return quotes


@router.post("/", response_model=QuoteResponse)
async def create_quote(
    *, session: Session = Depends(get_session), quote: QuoteRequest
):
    """
    Create a new quote in the database.

    This endpoint receives a quote via a POST request, stores it in the
    database, and returns the newly created quote along with its generated ID.

    Args:
        session (Session): The database session used to interact with the database.
        quote (QuoteRequest): A request body containing the author and text of the quote.

    Returns:
        QuoteResponse: The newly created quote, including the author, text, and ID.
    """
    # Convert the incoming request model to the database model
    quote_in_db = Quote.model_validate(quote)
    # Add the quote to the session and commit the transaction
    session.add(quote_in_db)
    session.commit()
    # Refresh the instance to get the generated ID from the database
    session.refresh(quote_in_db)
    # Return the created quote as a response
    return quote_in_db
