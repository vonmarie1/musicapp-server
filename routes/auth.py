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

from send_email import send_otp_email
router = APIRouter()

def generate_otp():
    return str(random.randint(100000, 999999))


@router.post('/signup', status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):

    user_db = db.query(User).filter(User.email == user.email).first()
    
    if user_db:
        raise HTTPException(400, 'User already exists')

    otp = generate_otp()  # Generate OTP
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    user_db = User(id=str(uuid.uuid4()), email=user.email, name=user.name, password=hashed_pw, otp=otp)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    # Send OTP using Mailgun
    if not send_otp_email(user.email, otp):
        raise HTTPException(500, "Failed to send OTP email")

    return {"message": "OTP sent. Please verify."}

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
      
@router.post('/verify-otp')
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.otp == otp).first()

    if not user:
        raise HTTPException(400, "Invalid OTP")

    user.otp = None
    db.commit()

    token = jwt.encode({'id': user.id}, 'password_key')

    return {'message': 'OTP verified', 'token': token}
