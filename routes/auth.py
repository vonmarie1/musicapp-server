import random
import uuid
import bcrypt
from fastapi import Depends, HTTPException
import requests
from database import get_db
from models.user import User
from schmas.usercreate import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session
from schmas.login import UserLogin
import jwt

router = APIRouter()



@router.post('/signup', status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(400, 'User already exists')

    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Create a new user object
    new_user = User(
        id=str(uuid.uuid4()),  # Generate a unique ID
        name=user.name,
        email=user.email,
        password=hashed_password  # Store hashed password
    )

    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return a success response
    return {"message": "User created successfully", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}

@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
      
      user_db = db.query(User).filter(User.email == user.email).first()

      if not user_db:
            raise HTTPException(400, 'User does not exist')
      
      is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

      if not is_match:
            raise HTTPException(400, 'Incorrect password')

      token = jwt.encode({'id': user_db.id}, 'password_key')
      
      return {'token': token, 'user': user_db}
      
