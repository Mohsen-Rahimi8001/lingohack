from fastapi import APIRouter, HTTPException, status, Depends

from dependencies.auth.login import get_current_active_user
from database.schemas import User, Table, TableCreate, PhraseCreate
from dependencies.phrase import get_table_dep, create_table_dep, delete_table_dep, create_phrase_dep

phrases_router = APIRouter(
    prefix="/tables",
    tags=["Phrases"]
)


@phrases_router.get("/")
async def read_tables(user: User = Depends(get_current_active_user)):
    tables = user.tables
    return tables


@phrases_router.get("/{table_id}")
async def read_table(table: Table = Depends(get_table_dep)):
    return table


@phrases_router.post("/")
async def create_table(table: TableCreate = Depends(create_table_dep)):
    return table


@phrases_router.delete("/{table_id}")
async def delete_table(table_id: int, user: User = Depends(get_current_active_user)):
    await delete_table_dep(table_id, user)
    return {
        "message": f"table with table id {table_id} deleted successfully"
    }

@phrases_router.get("/{table_id}/phrases")
async def read_phrases(table: Table = Depends(get_table_dep)):
    return table.phrases


@phrases_router.post("/{table_id}/phrases")
async def create_phrase(phrase: PhraseCreate = Depends(create_phrase_dep)):
    return phrase
