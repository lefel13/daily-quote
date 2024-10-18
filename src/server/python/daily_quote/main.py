from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import quotes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# FastAPI instance to define and serve the REST API.
app = FastAPI(lifespan=lifespan)
app.include_router(quotes.router)
