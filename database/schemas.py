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

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tables: list[Table] = []
    disabled: bool = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
