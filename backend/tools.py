import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

# --- TOOL 1: Get Seed Track Info ---
@tool
def get_seed_track_info(song_name, artist_name):
    """Searches Spotify to find the official track and artist IDs."""
    query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    
    if not results['tracks']['items']:
        return "Track not found."
        
    track = results['tracks']['items'][0]
    return {
        "track_name": track['name'],
        "track_id": track['id'],
        "artist_name": track['artists'][0]['name'],
        "artist_id": track['artists'][0]['id'],
        "spotify_url": track['external_urls']['spotify']
    }

# --- TOOL 2: Get Artist Genres ---
@tool
def get_artist_genres(artist_id)-> dict | str:
    """
    Fetches the official micro-genres for an artist from Spotify.
    WARNING: The artist_id MUST be the exact 22-character alphanumeric string 
    returned by the get_seed_track_info tool (e.g., '2CIMQHirSU0MQqyYHq0eOx'). 
    Do not guess or invent this ID.
    """
    try:
        artist = sp.artist(artist_id)
        return {
            "genres": artist.get('genres', [])
        }
    except spotipy.exceptions.SpotifyException as e:
        return f"Tool Error: The Spotify API rejected the artist_id '{artist_id}'. Ensure you are using the exact ID string from the previous step."
    except Exception as e:
        return f"Tool Error: {str(e)}"

# --- TOOL 3: Get Strict Recommendations (The Pivot) ---
@tool
def get_strict_recommendations(song_name, artist_name, limit=5):
    """Uses Last.fm to find highly similar tracks to prevent genre deviation."""
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getsimilar",
        "artist": artist_name,
        "track": song_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'similartracks' not in data or 'track' not in data['similartracks']:
        return "No similar tracks found."
        
    recommendations = []
    for track in data['similartracks']['track']:
        recommendations.append({
            "recommended_song": track['name'],
            "recommended_artist": track['artist']['name'],
            "match_score": track['match'] # A score from 0.0 to 1.0 indicating similarity
        })
        
    return recommendations

@tool
def get_similar_artist_tracks(artist_name: str, limit: int = 5) -> list | str:
    """
    FALLBACK TOOL: Use this if get_strict_recommendations returns nothing.
    It finds similar artists via Last.fm, then grabs a top track for each from Spotify.
    """
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getsimilar",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    
    try:
        # 1. Get Similar Artists from Last.fm
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'similarartists' not in data or 'artist' not in data['similarartists']:
            return "No similar artists found."
            
        similar_artists = [artist['name'] for artist in data['similarartists']['artist']]
        
        # 2. Search Spotify for a representative track from each similar artist
        recommendations = []
        for artist in similar_artists:
            # The Search API is still fully open to developers
            query = f"artist:{artist}"
            results = sp.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                recommendations.append({
                    "recommended_song": track['name'],
                    "recommended_artist": track['artists'][0]['name'],
                    "spotify_url": track['external_urls']['spotify'],
                    "match_type": "Similar Artist Recommendation"
                })
                
        return recommendations
    except Exception as e:
        return f"Fallback Tool Error: {str(e)}"

tools = [get_seed_track_info, get_artist_genres, get_strict_recommendations, get_similar_artist_tracks]