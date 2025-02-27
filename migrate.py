import json
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2

cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=musicapp user=postgres password=1234 host=localhost")
cursor = conn.cursor()

# Fetch users from PostgreSQL
cursor.execute("SELECT id, name, email FROM users;")
users = cursor.fetchall()

# Migrate to Firestore
for user in users:
    if len(user) == 3:  # If password is missing, set a default value
        user_id, name, email = user
        password = None  # Or set it to an empty string ""
    else:
        user_id, name, email, password = user

    if isinstance(password, bytes):  # Decode if it's binary
        password = password.decode("utf-8")

        
    db.collection("users").document(str(user_id)).set({
        "name": name,
        "email": email,
        "password": password,
    })
    print(f"User {name} migrated.")

# Close connection
cursor.close()
conn.close()
