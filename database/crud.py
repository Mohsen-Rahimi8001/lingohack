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


def get_table(db: Session, table_id: int):
    return db.query(models.Table).filter(models.Table.id == table_id).first()


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
