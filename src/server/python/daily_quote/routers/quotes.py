from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..quote_model import Quote, QuoteRequest, QuoteResponse
from ..database import get_session


router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("/", response_model=QuoteResponse)
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
