import logging
import uuid
import bcrypt
from fastapi import Depends, HTTPException
from database import get_firestore_db
from schmas.usercreate import UserCreate
from fastapi import APIRouter
from schmas.login import UserLogin
import jwt


router = APIRouter()



@router.post('/signup', status_code=201)
def signup_user(user: UserCreate):
    db = get_firestore_db()
    users_ref = db.collection("users")

    try:
        
        print("🔥 Connecting to Firestore...")

        
        user_doc = users_ref.where("email", "==", user.email).stream()
        if any(user_doc):
            print("❌ User already exists")
            raise HTTPException(400, "User already exists")

        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
        user_id = str(uuid.uuid4())

        
        users_ref.document(user_id).set({
            "name": user.name,
            "email": user.email,
            "password": hashed_password
        })

        print(f"✅ User {user.name} added to Firestore with ID {user_id}")
        return {"message": "User created successfully", "user": {"id": user_id, "name": user.name, "email": user.email}}

    except Exception as e:
        print(f"❌ Firestore Write Error: {e}")
        raise HTTPException(500, "Failed to save user to Firestore")



@router.post('/login')
def login_user(user: UserLogin):
    db = get_firestore_db()
    users_ref = db.collection("users")

    
    user_doc = users_ref.where("email", "==", user.email).stream()
    user_data = None
    for doc in user_doc:
        user_data = doc.to_dict()
        user_data["id"] = doc.id
        break

    if not user_data:
        raise HTTPException(400, 'User does not exist')

    
    is_match = bcrypt.checkpw(user.password.encode(), user_data["password"].encode())

    if not is_match:
        raise HTTPException(400, 'Incorrect password')

    
    token = jwt.encode({'id': user_data["id"]}, 'password_key')

    return {'token': token, 'user': user_data}


