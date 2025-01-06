from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel

load_dotenv()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

