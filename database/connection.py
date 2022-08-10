from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///./restaurant.db",
    connect_args={"check_same_thread": False},
    echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()