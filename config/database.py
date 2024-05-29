import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

engine=create_engine(os.getenv("DATABASE_URI", "sqlite:///database.db"), 
                        connect_args={"check_same_thread":False})

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    """Create A database session
    Yields:
        session: The database session
    """
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()