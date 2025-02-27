from fastapi import APIRouter
from database import get_firestore_db

router = APIRouter()

@router.get("/users")
async def get_users():
    db = get_firestore_db()
    users_ref = db.collection("users")  # Adjust to match your Firestore collection
    docs = users_ref.stream()

    users = []
    for doc in docs:
        users.append({"id": doc.id, **doc.to_dict()})

    return {"users": users}

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    db = get_firestore_db()
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        return {"id": user_doc.id, **user_doc.to_dict()}
    return {"error": "User not found"}
