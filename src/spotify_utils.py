"""
spotify_utils.py

Handles adjustify's spotify related tasks

Author: Travis Allen
02/24
"""
import os
from threading import Timer
import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyOAuth

class SpotifyUtils():
    def __init__(self):
        ## create client, load list of artists to skip
        self.client = self.create_client()
        self.load_skip_artists()


    def create_client(self):
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


    def load_skip_artists(self):
        """
        Loads and stores artists to skip. Artists must be in a .csv file
        whose relative path is: '../skip/skip_artists.csv' and whose contents
        are:

        artist 1
        artist 2
        ...

        Args:
        - None

        Returns:
        - None
        """
        path = os.path.join('..','skip','skip_artists.csv')
        skip_artists = np.loadtxt(path, dtype=str, delimiter=',')
        self.skip_artists = list(skip_artists)

        
    def pause_after_this_song(self,client: spotipy.Spotify) -> None:
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

        time_remaining = float(cp["item"]["duration_ms"] - cp["progress_ms"])/1000.0
        t = Timer(time_remaining,client.pause_playback,args=None,kwargs=None)
        t.start()

        
    def artist_skip(self,client: spotipy.Spotify, artist: str) -> None:
        """
        Skips track if its artist is `artist`

        Args:
        - client: spotipy client for whom the operation will be performed
        - artist: string containing the name of the artist to skip

        Returns:
        - None
        """
        cp = client.current_playback()
        if cp["item"]["artists"][0]["name"] in self.skip_artists:
            client.next_track()