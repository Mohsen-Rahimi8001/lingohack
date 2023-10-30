import os
from dotenv import load_dotenv
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import pwd_context
from database.schemas import User, UserCreate, TokenData

from database.crud import get_user_by_username, create_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    db = next(get_db())
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_refresh_token(data: dict, access_exp: timedelta | None = None, refresh_exp: timedelta | None = None):
    access_token_data = data.copy()
    refresh_token_data = data.copy()

    if access_exp:
        access_expire = datetime.utcnow() + access_exp
    else:
        eaccess_expir = datetime.utcnow() + timedelta(minutes=15)

    if refresh_exp:
        refresh_expire = datetime.utcnow() + refresh_exp
    else:
        refresh_expire = datetime.utcnow() + timedelta(days=90)

    access_token_data.update({"exp": access_expire})
    access_token_data.update({"iat": datetime.utcnow()})
    access_token_data = jwt.encode(
        access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    refresh_token_data.update({"exp": refresh_expire})
    refresh_token_data.update({"iat": datetime.now()})
    refresh_token_data = jwt.encode(refresh_token_data, SECRET_KEY, ALGORITHM)

    return access_token_data, refresh_token_data


def renew_access_token(refresh_token: str):
    data = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
    data["exp"] = datetime.utcnow() + timedelta(minutes=15)

    new_access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return new_access_token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    db = next(get_db())
    user = get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
