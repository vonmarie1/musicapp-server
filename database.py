import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("service-account.json")  # Make sure this file is correct
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def get_firestore_db():
    return db