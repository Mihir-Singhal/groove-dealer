import json
import re
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent import run_music_pipeline, is_safe_prompt
from tools import sp
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

app = FastAPI(
    title="Agentic Music Recommender API",
    description="An AI agent that fetches curated electronic music recommendations.",
    version="1.0.0"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:5173", # for local testing
    "https://groove-dealer.vercel.app" # VERCEL URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class MusicRequest(BaseModel):
    user_prompt: str

@app.post("/api/recommend")
@limiter.limit("5/minute")
async def get_recommendations(request: Request, music_req: MusicRequest):
    try:
        
        if not is_safe_prompt(music_req.user_prompt):
            raise HTTPException(
                status_code=400, 
                detail="Security alert: Request was flagged as invalid or unsafe."
            )

        # Run the 3-stage pipeline 
        parsed_json = run_music_pipeline(music_req.user_prompt)
        
        # Spotify Data Hydration
        for track in parsed_json:
            search_query = f"track:{track['title']} artist:{track['artist']}"
            try:
                spotify_results = sp.search(q=search_query, type='track', limit=1)
                if spotify_results['tracks']['items']:
                    spotify_data = spotify_results['tracks']['items'][0]
                    track['spotify_url'] = spotify_data['external_urls']['spotify']
                    if spotify_data['album']['images']:
                        track['image_url'] = spotify_data['album']['images'][0]['url']
            except Exception as e:
                print(f"Spotify search failed for {track['title']}: {e}")
        
        # Send it to React
        return {"recommendations": parsed_json}
            
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Backend execution failed: {str(e)}")
if __name__ == "__main__":
    import uvicorn
    # Runs the API on http://localhost:8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)