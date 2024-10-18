# database.py
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
This module handles the creation and connection to the SQLite database
for the 'daily_quote' project.

It includes the necessary functions to create the database tables
and manage database sessions.
"""

from sqlmodel import Session, SQLModel, create_engine

# Database file and connection URL for SQLite.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Disable 'check_same_thread' to prevent issues with thread handling in FastAPI.
# Each request in FastAPI can be handled by multiple interacting threads.
connect_args = {"check_same_thread": False}

# Create the database engine, which manages connections to the SQLite database.
# The 'echo=True' parameter logs SQL statements, useful for debugging.
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """
    Create the database and tables.

    This function initializes the database schema by creating all
    tables defined in the SQLModel models.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Provide a database session.

    This function yields a new database session for use in database transactions.
    It ensures that the session is properly cleaned up and closed after use.

    Yields:
        Session: An active SQLModel session connected to the SQLite database.
    """
    with Session(engine) as session:
        yield session
