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

from fastapi import FastAPI
from pydantic import BaseModel


class Quote(BaseModel):
    """
    A model representing a quote with an author and text.

    Attributes:
        author (str): The author of the quote.
        text (str): The content of the quote.
    """
    author: str
    text: str


app = FastAPI()


@app.post("/quotes/")
async def create_quote(quote: Quote):
    """
    Create a new quote.

    This endpoint allows users to post a new quote, providing the author
    and the text.

    Args:
        quote (Quote): A Quote object containing the author and text of the quote.

    Returns:
        Quote: The newly created quote object.
    """
    return quote
