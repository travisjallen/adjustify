"""
spotify_utils.py

Handles adjustify's spotify related tasks

Author: Travis Allen
02/24
"""
import os
import time
import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyOAuth

def create_client():
    """
    Creates a spotipy client. Requires a file called 'client.csv' whose
    relative path is: '../client/client.csv' and whose contents are 
    
    client_id,client_secret
    
    Args: 
    - None

    Returns:
    - spotipy client object
    """
    path = os.path.join('..','client','client.csv')
    client_info = np.loadtxt(path, dtype=str, delimiter=',')
    scope = 'user-read-playback-state,user-modify-playback-state'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_info[0],
                                               client_secret=client_info[1],
                                               redirect_uri="http://localhost:1234",
                                               scope=scope))
    return sp
    
def pause_after_this_song(client: spotipy.Spotify) -> None:
    """
    Pauses spotify after the completion of the current song.

    Args:
    - client: spotipy client for whom the operation will be performed

    Returns:
    - None
    """
    cp = client.current_playback()
    if cp["is_playing"] is False:
        return

    time_remaining = cp["item"]["duration_ms"] - cp["progress_ms"]
    time.sleep(float(time_remaining)/1000.0)
    client.pause_playback()
    
def artist_skip(client: spotipy.Spotify, artist: str) -> None:
    """
    Skips track if its artist is `artist`

    Args:
    - client: spotipy client for whom the operation will be performed
    - artist: string containing the name of the artist to skip

    Returns:
    - None
    """
    cp = client.current_playback()
    if cp["item"]["artists"][0]["name"] == artist:
        client.next_track()