from fastapi import APIRouter, HTTPException, status, Depends

from database.schemas import User, Quiz
from dependencies.user import get_current_active_user
from dependencies.quiz import load_quiz, get_quiz_dep, delete_quiz_dep, recieve_answers_dep

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@quiz_router.get("/new_quiz")
async def get_new_quiz(quiz: Quiz = Depends(load_quiz)):
    return quiz


@quiz_router.get("/{quiz_id}")
async def get_quiz_by_id(quiz: Quiz = Depends(get_quiz_dep)):
    # load quiz questions
    for question in quiz.questions:
        question.choices = question.choices

    quiz.difficulty
    
    return quiz


@quiz_router.get("/")
async def get_all_quizzes(user: User = Depends(get_current_active_user)):
    quizzes = user.quizzes
    return quizzes


@quiz_router.delete("/{quiz_id}")
async def delete_quiz(quiz: Quiz = Depends(delete_quiz_dep)):
    return quiz


@quiz_router.post("/submit_answer")
async def submit_answer(score: float = Depends(recieve_answers_dep)):
    return {
        "score": score
    }