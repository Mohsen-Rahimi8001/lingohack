from sqlalchemy.orm import Session

from . import schemas, models

from database import pwd_context


def get_user(db: Session, user_id: int):
    return db.query(models.User).\
        filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).\
        filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_table(db: Session, table_id: int, user_id: int):
    return db.query(models.Table).filter(models.Table.id == table_id, models.Table.writer_id == user_id).first()


def create_table(db: Session, table: schemas.TableCreate, user: schemas.User):
    db_table = models.Table(
        writer_id=user.id,
        title=table.title,
        description=table.description,
        difficulty=table.difficulty
    )

    db.add(db_table)
    db.commit()
    db.refresh(db_table)

    return db_table


def delete_table(db: Session, table: schemas.Table):
    db.delete(table)
    db.commit()


def create_phrase(db: Session, phrase: schemas.PhraseCreate, table: schemas.Table):
    db_phrase = models.Phrase(
        table_id=table.id,
        phrase=phrase.phrase,
        meaning=phrase.meaning,
        description=phrase.description,
        difficulty=phrase.difficulty
    )

    db.add(db_phrase)
    db.commit()
    db.refresh(db_phrase)

    return db_phrase


def get_quiz(db: Session, quiz_id: int, user_id: int):
    return db.query(models.Quiz).\
        filter(models.Quiz.id == quiz_id, models.Quiz.participant_id == user_id)\
        .first()


def get_quizzes(db: Session, user_id: int, limit: int = 100, skip: int = 0):
    return db.query(models.Quiz).\
        filter(models.Quiz.participant_id == user_id).\
        offset(skip).limit(limit).all()


def create_quiz(db: Session, quiz: schemas.QuizCreate, user_id: int):
    db_quiz = models.Quiz(
        participant_id=user_id,
        title=quiz.title,
        description=quiz.description,
    )

    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    return db_quiz


def delete_quiz(db: Session, quiz: schemas.Quiz):
    db.delete(quiz)
    db.commit()


def read_questions(db: Session, user_id: int, limit: int = 100, skip: int = 0):
    return db.query(models.Question).\
        filter(models.Question.quiz.participant_id == user_id).\
        offset(skip).limit(limit).all()


def read_tables(db: Session, user_id: int, limit: int = 100, skip: int = 0):
    return db.query(models.Table).\
        filter(models.Table.writer_id == user_id).\
        offset(skip).limit(limit).all()


def create_choice(db: Session, choice: schemas.ChoiceCreate, question_id: int):
    db_choice = models.Choice(
        question_id=question_id,
        text=choice.text,
        is_correct=choice.is_correct
    )

    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)

    return db_choice


def create_question(db: Session, question: schemas.QuestionCreate, quiz_id: int):
    db_question = models.Question(
        quiz_id=quiz_id,
        question=question.question
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question
