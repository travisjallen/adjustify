"""
main.py

Runs adjustify.

Travis Allen
02/24
"""
import os
# import spotipy
# import numpy as np
import spotify_utils
def main():
    os.system('clear')
    sp = spotify_utils.create_client()
    spotify_utils.pause_after_this_song(sp)
    spotify_utils.artist_skip(sp,"Bahamas")

if __name__ == '__main__':
    main()