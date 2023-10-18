from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float
)
from sqlalchemy.orm import relationship


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    tables = relationship("Table", back_populates="writer",
                          cascade="all, delete-orphan, delete")


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    difficulty = Column(Float, default=0)

    writer_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    writer = relationship("User", back_populates="tables")

    phrases = relationship("Phrase", back_populates="table",
                           cascade="all, delete-orphan, delete")


class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, index=True)
    meaning = Column(String, index=True)
    description = Column(String, index=True)
    difficulty = Column(Float, default=0)

    table_id = Column(Integer, ForeignKey(
        "tables.id", ondelete="CASCADE"), nullable=False)

    table = relationship("Table", back_populates="phrases")
