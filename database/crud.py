from sqlalchemy.orm import Session

from . import schemas, models

from database import pwd_context


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


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
