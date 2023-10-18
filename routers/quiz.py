from fastapi import APIRouter, HTTPException, status, Depends

from database.schemas import User, Quiz
from dependencies.user import get_current_active_user
from dependencies.quiz import load_quiz

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@quiz_router.get("/")
async def get_quiz(quiz: Quiz = Depends(load_quiz), user: User = Depends(get_current_active_user)):
    return quiz
