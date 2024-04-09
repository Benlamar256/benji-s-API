from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://smarthemocheck_user:z9XvkbUosAtRpSISUL2BlT6U3DBhIVvL@dpg-coaga5779t8c73ehlu1g-a.oregon-postgres.render.com/smarthemocheck'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def init_db():
    async with engine.begin() as conn:
        from .model import User, Post
        await conn.run_sync(Base.metadata.create_all)

        return init_db

     