from fastapi import Depends, FastAPI
from routers import auth_router, phrases_router, quiz_router
from database import models
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(phrases_router)
app.include_router(quiz_router)
