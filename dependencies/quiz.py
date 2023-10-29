from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from database.database import SessionLocal

from database.crud import (
    read_tables, 
    create_choice, 
    create_question, 
    create_quiz,
    get_quiz,
    delete_quiz
)

from database.schemas import (
    User, 
    Question,
    Choice,
    Quiz,
    QuestionCreate, 
    ChoiceCreate, 
    QuizCreate,
    Phrase
)

from .user import get_current_active_user

import random


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_quiz_dep(quiz_id: int, user: User = Depends(get_current_active_user)):

    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"quiz with quiz id {quiz_id} not found"
    )

    db = next(get_db())
    quiz = get_quiz(db, quiz_id, user.id)

    if not quiz:
        raise not_found_exception
    
    return quiz


async def delete_quiz_dep(quiz_id: int, user: User = Depends(get_current_active_user)):
    
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"quiz with quiz id {quiz_id} not found"
    )

    db = next(get_db())
    quiz = get_quiz(db, quiz_id, user.id)

    if not quiz:
        raise not_found_exception
    
    quiz_to_show = quiz.dict()

    delete_quiz(db, quiz)

    return quiz_to_show


async def load_quiz(title:str, description:str, user: User = Depends(get_current_active_user)):
    db = next(get_db())
    # create some questions
    tables = read_tables(db, user.id)

    if not len(tables):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have any tables yet"
        )

    # choose 5 question randomly for now
    phrases: list[Phrase] = []

    for table in tables:
        phrases.extend(table.phrases)

    random.shuffle(phrases)

    result_quiz = QuizCreate(
        title=title,
        description=description,
        participant_id=user.id
    )

    result_quiz = create_quiz(db, result_quiz, user.id)

    questions : list[Question] = []

    if len(phrases) < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need at least 5 phrases to create a quiz"
        )

    for i, phrase in enumerate(phrases[:5]):
        q = QuestionCreate(
            question=f"What is the meaning of {phrase.phrase}?"
        )

        q_in_db = create_question(db, q, result_quiz.id)

        choices_to_create : list[ChoiceCreate] = [
            ChoiceCreate(
                text = phrase.meaning,
                is_correct = True
            )
        ]

        # pick 3 random phrases except the current phrase
        random_phrases = phrases[:i] + phrases[i+1:]
        random.shuffle(random_phrases)
        random_phrases = random_phrases[:3]

        for random_phrase in random_phrases:
            choices_to_create.append(
                ChoiceCreate(
                    text = random_phrase.meaning,
                    is_correct = False
                )
            )
        
        random.shuffle(choices_to_create)

        # create choices
        choices_in_db : list[Choice] = []

        for choice in choices_to_create:
            choices_in_db.append(
                create_choice(db, choice, q_in_db.id)
            )

    
        q_in_db.choices = choices_in_db.copy()

        questions.append(q_in_db)
    
    result_quiz.questions = questions.copy()

    return result_quiz
