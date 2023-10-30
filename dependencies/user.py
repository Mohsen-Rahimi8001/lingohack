import os
from dotenv import load_dotenv
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt, exceptions

from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import pwd_context
from database.schemas import User, UserCreate, TokenData, TokenRecieve, Token

from database.crud import get_user_by_username, create_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def access_token_expiration_time():
    return datetime.utcnow() + timedelta(minutes=30)


def refresh_token_expiration_time():
    return datetime.utcnow() + timedelta(days=7)


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


def create_access_refresh_token(data: dict):
    access_token_data = data.copy()
    refresh_token_data = data.copy()

    access_expire = access_token_expiration_time()
    refresh_expire = refresh_token_expiration_time()

    access_token_data.update({"exp": access_expire})
    access_token_data.update({"iat": datetime.utcnow()})
    access_token_data = jwt.encode(
        access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    refresh_token_data.update({"exp": refresh_expire})
    refresh_token_data.update({"iat": datetime.utcnow()})
    refresh_token_data = jwt.encode(refresh_token_data, SECRET_KEY, ALGORITHM)

    return access_token_data, refresh_token_data


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


def renew_access_token(refresh_token: TokenRecieve = Body(...)):
    try:
        data = jwt.decode(refresh_token.refresh, SECRET_KEY, ALGORITHM)

    except (exceptions.JWTError | exceptions.ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )

    data["exp"] = refresh_token_expiration_time()

    new_access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    
    return Token(
        token=new_access_token,
        token_type="bearer"
    )
