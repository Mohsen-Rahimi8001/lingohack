from datetime import timedelta

from fastapi import APIRouter, Body, HTTPException, status, Depends

from fastapi.security import OAuth2PasswordRequestForm

from dependencies.user import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    register_user as register_user_dep
)

from database.schemas import Token, User

auth_router = APIRouter(tags=["User"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60 


@auth_router.post("/token", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register")
async def register_user(username: str = Body(...), password: str = Body(...), confirmPasswd: str = Body(...)):
    if password != confirmPasswd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="password and confirm password should be the same"
        )

    created_user = await register_user_dep(username, password)

    return {
        "message": f"user {created_user.username} is successfully created"
    }


@auth_router.get("/me")
async def get_me(user: User = Depends(get_current_active_user)):
    response = {
        "id": user.id,
        "username": user.username,
        "tables": [table.title for table in user.tables],
        "quizzes": [quiz.title for quiz in user.quizzes],
        "disabled": user.disabled
    }
    return response
