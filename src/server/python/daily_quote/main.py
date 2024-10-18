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

"""
This module defines the FastAPI application for the 'daily_quote' project.

The application handles creating the database, managing the application lifespan,
and routing requests for managing quotes.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import quotes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application's lifespan.

    This function is used to handle actions required when the application starts
    and stops, such as creating the database tables.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    create_db_and_tables()
    yield


# FastAPI instance to define and serve the REST API.
app = FastAPI(lifespan=lifespan)

# Include the quotes router to handle the '/quotes' endpoints.
app.include_router(quotes.router)
