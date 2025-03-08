from fastapi import FastAPI, HTTPException, Depends
import requests
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router 
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YOUTUBE_API_KEY = "AIzaSyBY_WjeIpY_Vmv_P3-9cSFy8Vn4xiYufYg"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"


def get_current_user(authorization: str = Depends(auth.verify_id_token)):
    return authorization

@app.get("/search-youtube")
def search_youtube(query: str):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",  # Music category
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to fetch data from YouTube")

@app.get("/quick-picks")
def get_quick_picks(current_user: dict = Depends(get_current_user)):
    # In a real app, you might base this on user preferences or trending videos
    return search_youtube("popular music")['items'][:10]

@app.get("/recently-played")
def get_recently_played(current_user: dict = Depends(get_current_user)):
    # In a real app, you would fetch this from a database based on user's history
    # For now, we'll just return some placeholder data
    return search_youtube("top hits")['items'][:10]

@app.get("/recommendations")
def get_recommendations(current_user: dict = Depends(get_current_user)):
    # In a real app, you would use a recommendation algorithm
    # For now, we'll just return some placeholder data
    return search_youtube("recommended music")['items'][:10]

@app.get("/")
def read_root():
    return {"message": "API is running"}

