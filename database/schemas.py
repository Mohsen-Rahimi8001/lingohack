from pydantic import BaseModel


class PhraseBase(BaseModel):
    phrase: str
    meaning: str
    description: str


class PhraseCreate(PhraseBase):
    pass


class Phrase(PhraseBase):
    id: int
    table_id: int
    difficulty: float
    questions: list = []

    class Config:
        from_attributes = True


class PhraseUpdate(PhraseBase):
    ask_count: int = 0
    correct_answers: int = 0


class TableBase(BaseModel):
    title: str
    description: str


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int
    writer_id: int
    phrases: list[Phrase] = []
    difficulty: float

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tables: list[Table] = []
    quizzes: list = []
    disabled: bool = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    token: str
    token_type: str


class TokenRecieve(BaseModel):
    refresh: str


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
    phrase_id: int


class Question(QuestionBase):
    id: int
    quiz_id: int
    choices: list[Choice] = []
    phrase_id: int

    class Config:
        from_attributes = True


class QuestionUpdate(QuestionBase):
    ask_count: int = 0
    correct_answers: int = 0


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


class Answer(BaseModel):
    question_id: int
    choice_id: int
