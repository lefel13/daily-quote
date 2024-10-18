from sqlmodel import Session, SQLModel, create_engine

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
