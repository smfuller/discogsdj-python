import os
import requests

from datetime import datetime


class Spotify:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    bearer_token = os.getenv("SPOTIFY_MY_BEARER_TOKEN")
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
    username = os.getenv("SPOTIFY_USERNAME")

    playlist_uri = f"https://api.spotify.com/v1/users/{username}/playlists"
    search_uri = "https://api.spotify.com/v1/search"
    update_uri = "https://api.spotify.com/v1/playlists"
    albums_uri = "https://api.spotify.com/v1/albums"

    headers = {'Authorization': f'Bearer {bearer_token}'}

    def get_search_json(self, album):
        j = requests.get(f"{self.search_uri}?q={album}&type=album", headers=self.headers)
        return j

    # TODO -- mirror remaining Spotify connector code from Kotlin version
    def create_playlist(self):
        now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        playlist_json = {
            "name": f"DiscogsDJ - {now}",
            "description": "Created by DiscogsDJ",
            "public": "false"
        }
        print(playlist_json)
        j = requests.post(self.playlist_uri, headers=self.headers, json=playlist_json)
        return j

    def add_to_playlist(self, uris, playlist):
        body_json = {
            "uris": uris
        }
        j = requests.post(f"{self.update_uri}/{playlist}/tracks", headers=self.headers, json=body_json)
        return j

    def get_tracks(self, uri):
        clean_uri = uri.replace("spotify:album:", "")
        j = requests.get(f"{self.albums_uri}/{clean_uri}/tracks", headers=self.headers)
        return j.json()
