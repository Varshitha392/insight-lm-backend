from fastapi import FastAPI

from app.database.database import engine, Base

from app.models.user import User
from app.models.module import Module
from app.models.file import File

from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.module import router as module_router
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(module_router)
app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "SourceMind AI Backend Running"
    }