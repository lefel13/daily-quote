from sqlmodel import SQLModel, Field
from typing import Optional


class QuoteBase(SQLModel):
    author: str
    text: str


class Quote(QuoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class QuoteRequest(QuoteBase):
    pass


class QuoteResponse(QuoteBase):
    id: int
