from fastapi import FastAPI
from pydantic import BaseModel
from models.base import Base
from database import engine
from routes import auth


app = FastAPI()

app.include_router(auth.router, prefix='/auth')

Base.metadata.create_all(engine)