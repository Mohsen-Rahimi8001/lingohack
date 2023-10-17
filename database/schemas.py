from pydantic import BaseModel


class PhraseBase(BaseModel):
    phrase: str
    meaning: str
    description: str
    difficulty: str


class PhraseCreate(PhraseBase):
    pass


class Phrase(PhraseBase):
    id: int
    table_id: int

    class Config:
        orm_mode = True


class TableBase(BaseModel):
    title: str
    description: str
    difficulty: float


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int
    writer_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tables: list[Table] = []

    class Config:
        orm_mode = True
