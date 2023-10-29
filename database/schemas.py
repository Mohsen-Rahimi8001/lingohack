from pydantic import BaseModel


class PhraseBase(BaseModel):
    phrase: str
    meaning: str
    description: str
    difficulty: float


class PhraseCreate(PhraseBase):
    pass


class Phrase(PhraseBase):
    id: int
    table_id: int

    class Config:
        from_attributes = True


class TableBase(BaseModel):
    title: str
    description: str
    difficulty: float


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int
    writer_id: int
    phrases: list[Phrase] = []

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tables: list[Table] = []
    quizzes: list['Quiz'] = []
    disabled: bool = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ChoiceBase(BaseModel):
    text: str
    is_correct: bool


class ChoiceCreate(ChoiceBase):
    pass


class Choice(ChoiceBase):
    question_id: int

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    question: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    quiz_id: int
    choices: list[Choice] = []

    class Config:
        from_attributes = True


class QuizBase(BaseModel):
    title: str
    description: str


class QuizCreate(QuizBase):
    pass


class Quiz(QuizBase):
    id: int
    participant_id: int
    questions: list[Question] = []
    difficulty: float
    total_score: int

    class Config:
        from_attributes = True
