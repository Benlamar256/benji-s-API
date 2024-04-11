from contextlib import asynccontextmanager
from .config import settings
from .database import init_db
from fastapi import FastAPI




#lifespan code


@asynccontextmanager

async def lifespan(app:FastAPI):
    await init_db()

    yield
    
    def create_app():
        app = FastAPI(
        description="this good Stuff",
        title="smartHemocheck",
        version=settings.VERSION,
        lifespan=lifespan)
        return app