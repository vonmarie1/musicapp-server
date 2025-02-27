from fastapi import FastAPI
from routes import auth
from models.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware  
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/auth')
app.include_router(user_router, prefix='/users')  # Include user routes

print("Backend is running with Firestore")