import json
import os
import re
import requests
import time

from album import Album
from spotify import Spotify

discogs_oauth_key = os.getenv("DISCOGS_CONSUMER_KEY")
discogs_oauth_secret = os.getenv("DISCOGS_CONSUMER_SECRET")
discogs_key = os.getenv('DISCOGS_MY_ACCESS_SECRET')
discogs_token = os.getenv('DISCOGS_MY_ACCESS_TOKEN')
discogs_username = os.getenv('DISCOGS_USERNAME')

collection_uri = f"https://api.discogs.com/users/{discogs_username}/collection"

oauth = f'OAuth oauth_consumer_key="{discogs_oauth_key}",oauth_token="{discogs_token}",' \
        'oauth_signature_method="HMAC-SHA1",' \
        'oauth_version="1.0"'

headers = {'Authorization': oauth}


def get_next_page_json(json_object, json_list):
    print("Adding a json object...")
    json_list.append(json_object)
    if "next" in json_object["pagination"]["urls"]:
        next_page = json_object["pagination"]["urls"]["next"]
        get_next_page_json(requests.get(next_page, headers=headers).json(), json_list)
    return json_list


def main():
    j = requests.get(collection_uri, headers=headers).json()

    json_list = []
    collection_list = get_next_page_json(j, json_list)

    album_list = []
    clean_album_list = []

    for i in collection_list:
        for x in i["releases"]:
            artist = x["basic_information"]["artists_sort"]
            album = x["basic_information"]["title"]
            album_list.append(Album(artist, album))

    for i in album_list:
        clean_artist = re.sub(r" \(\d*\)", "", i.artist)
        track = f"{clean_artist}+{i.title}".replace(" ", "+")
        if track not in clean_album_list:
            clean_album_list.append(track)

    s = Spotify()
    playlist = s.create_playlist()

    if playlist.status_code == 201:
        playlist_id = playlist.json()["id"]
        album_uris = []
        track_uris = []
        print(f"\nPlaylist {playlist_id} created! Looking for songs to add to it...")

        for album in clean_album_list:
            album_query = s.get_search_json(album).json()["albums"]["items"]
            if len(album_query) > 0:
                album_uris.append(album_query[0]["uri"])

        for uri in album_uris:
            tracks_json = json.dumps(s.get_tracks(uri))
            track_uris += (re.findall("spotify:track:.[^\"]*", tracks_json))

        print(f"\n{len(track_uris)} songs found. Adding...")

        while len(track_uris) > 100:
            s.add_to_playlist(track_uris[:99], playlist_id)
            track_uris = track_uris[100:]

        s.add_to_playlist(track_uris, playlist_id)
        print("Done, check your Spotify account!")

    elif playlist.status_code == 401:
        print("Your bearer token has expired...")
    else:
        print("If you're seeing this message, something has gone very wrong")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Done in {time.time() - start_time} seconds.")
