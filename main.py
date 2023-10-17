from fastapi import FastAPI
from routers.auth import auth_router
from database import models
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

