import firebase_admin
from firebase_admin import auth, credentials


cred = credentials.Certificate("service-account.json")  
firebase_admin.initialize_app(cred)

def delete_all_users():
    users = auth.list_users().iterate_all()
    for user in users:
        auth.delete_user(user.uid)
        print(f"✅ Deleted user: {user.email}")

if __name__ == "__main__":
    delete_all_users()
    print("🔥 All users deleted successfully.")
