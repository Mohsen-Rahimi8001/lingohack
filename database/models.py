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

    quizzes = relationship("Quiz", back_populates="participant",
                           cascade="all, delete-orphan, delete")


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    writer_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    writer = relationship("User", back_populates="tables")

    phrases = relationship("Phrase", back_populates="table",
                           cascade="all, delete-orphan, delete")

    @property
    def difficulty(self):
        if len(self.phrases) == 0:
            return 0

        res = 0
        for phrase in self.phrases:
            res += phrase.difficulty

        return res / len(self.phrases)


class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, index=True)
    meaning = Column(String, index=True)
    description = Column(String, index=True)

    ask_count = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)

    table_id = Column(Integer, ForeignKey(
        "tables.id", ondelete="CASCADE"), nullable=False)

    table = relationship("Table", back_populates="phrases")

    questions = relationship(
        "Question", back_populates="phrase", cascade="all, delete-orphan, delete")

    @property
    def difficulty(self):
        if self.ask_count == 0:
            return 0

        return self.correct_answers / self.ask_count


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    total_score = Column(Integer, default=0)

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan, delete")

    participant_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    participant = relationship("User", back_populates="quizzes")

    @property
    def difficulty(self):
        if len(self.questions) == 0:
            return 0

        res = 0
        for question in self.questions:
            res += question.difficulty

        return res / len(self.questions)

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "total_score": self.total_score,
            "participant_id": self.participant_id,
        }


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)

    ask_count = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)

    phrase_id = Column(Integer, ForeignKey(
        "phrases.id", ondelete="CASCADE"), nullable=False)

    phrase = relationship("Phrase", back_populates="questions")

    quiz_id = Column(Integer, ForeignKey(
        "quizzes.id", ondelete="CASCADE"), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")

    choices = relationship("Choice", back_populates="question",
                           cascade="all, delete-orphan, delete")

    @property
    def difficulty(self):
        if self.ask_count == 0:
            return 0
            
        return self.correct_answers / self.ask_count


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"), nullable=False)

    question = relationship("Question", back_populates="choices")
