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

from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..quote_model import Quote, QuoteRequest, QuoteResponse
from ..database import get_session

# Define the router for handling quote-related operations.
router = APIRouter(prefix="/quotes", tags=["quotes"])


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
