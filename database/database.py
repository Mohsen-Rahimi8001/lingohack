from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(filename="sqlalchemy.log")
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

SQLASQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLASQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()