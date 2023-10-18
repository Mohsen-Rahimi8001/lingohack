from fastapi import APIRouter, HTTPException, status, Depends

from dependencies.auth.login import get_current_active_user
from database.schemas import User, Table, TableCreate
from dependencies.phrase import get_table_dep, create_table_dep

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
