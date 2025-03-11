import logging
from fastapi import FastAPI, HTTPException, Depends
import requests
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from models.user import router as user_router
from firebase_admin import auth, credentials, initialize_app, exceptions
from database import db

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Flutter app's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YOUTUBE_API_KEY = "AIzaSyBY_WjeIpY_Vmv_P3-9cSFy8Vn4xiYufYg"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

# Firebase authentication dependency
def get_current_user(authorization: str = Depends(auth.verify_id_token)):
    try:
        return authorization
    except exceptions.FirebaseError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication token")

# Email verification status check
@app.get("/auth/check-verification")
def check_email_verification(current_user: dict = Depends(get_current_user)):
    user = auth.get_user(current_user['uid'])
    return {"email_verified": user.email_verified}

# YouTube search endpoint
@app.get("/search-youtube")
def search_youtube(query: str):
    logger.info(f"Searching YouTube for: {query}")
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    logger.error(f"Failed to fetch from YouTube: {response.text}")
    raise HTTPException(status_code=500, detail="Failed to fetch data from YouTube")

# Additional endpoints using current_user dependency
@app.get("/quick-picks")
def get_quick_picks(current_user: dict = Depends(get_current_user)):
    return search_youtube("popular music")['items'][:10]

@app.get("/recently-played")
def get_recently_played(current_user: dict = Depends(get_current_user)):
    return search_youtube("top hits")['items'][:10]

@app.get("/recommendations")
def get_recommendations(current_user: dict = Depends(get_current_user)):
    return search_youtube("recommended music")['items'][:10]

@app.get("/")
def read_root():
    return {"message": "API is running"}
