from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.crud import get_table, create_table, delete_table, create_phrase
from database.schemas import TableCreate, Table, User, PhraseCreate

from .user import get_current_active_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_table_dep(table_id: int, user: User = Depends(get_current_active_user)):
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"table with table id {table_id} not found"
    )

    db = next(get_db())
    table = get_table(db, table_id, user.id)

    if not table:
        raise not_found_exception

    return table


async def create_table_dep(title: str, description: str, user: User = Depends(get_current_active_user)):
    db = next(get_db())
    table = TableCreate(
        title=title,
        description=description,
    )

    table = create_table(db, table, user)

    return table


async def delete_table_dep(table_id: int, user: User = Depends(get_current_active_user)):
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"table with table id {table_id} not found"
    )

    db = next(get_db())
    table = get_table(db, table_id, user.id)

    if not table:
        raise not_found_exception

    delete_table(db, table)


async def create_phrase_dep(table_id: int, phrase: PhraseCreate, user: User = Depends(get_current_active_user)):
    db = next(get_db())
    table = get_table(db, table_id, user.id)

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"table with table id {table_id} not found"
        )

    phrase = create_phrase(db, phrase, table)

    return phrase
