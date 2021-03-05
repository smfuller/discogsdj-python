import os
import requests
import re


class Spotify:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    bearer_token = os.getenv("SPOTIFY_MY_BEARER_TOKEN")
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
    username = os.getenv("SPOTIFY_USERNAME")

    playlist_uri = f"https://api.spotify.com/v1/users/{username}/playlists"
    search_uri = "https://api.spotify.com/v1/search"
    update_uri = "https://api.spotify.com/v1/playlists"

    def get_search_json(self, artist, album):
        cleanup = re.sub(r' ', '+', f'{artist}+{album}')
        headers = {'Authorization': f'Bearer {self.bearer_token}'}
        j = requests.get(f"{self.search_uri}?q={cleanup}&type=album", headers=headers)
        return j.json()

    # TODO -- mirror remaining Spotify connector code from Kotlin version
