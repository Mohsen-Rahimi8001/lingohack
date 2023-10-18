from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
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


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    difficulty = Column(Float, default=0)
    total_score = Column(Integer, default=0)

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan, delete")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(Integer)

    quiz_id = Column(Integer, ForeignKey(
        "quizzes.id", ondelete="CASCADE"), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")

    choices = relationship("Choice", back_populates="question",
                           cascade="all, delete-orphan, delete")


class Choice(Base):
    __tablename__ = "choices"

    text = Column(String, index=True)
    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    question = relationship("Question", back_populates="choices")
