from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.crud import create_user, get_user_by_username
from database.schemas import UserCreate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def register_user(username: str, password: str):
    db = next(get_db())
    user = get_user_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this username already exists"
        )

    to_create_user = UserCreate(
        username=username, password=password
    )
    created_user = create_user(db, to_create_user)
    return created_user
