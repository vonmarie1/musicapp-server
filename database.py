import firebase_admin
from firebase_admin import credentials, firestore
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(current_dir, "service-account.json")


try:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized successfully")
except ValueError as e:
    print(f"❌ Firebase initialization error: {e}")
    print("Make sure your service-account.json file is correctly formatted")



db = firestore.client()

def get_firestore_db():
    return db