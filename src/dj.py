import os
import requests

from song import Song
from spotify import Spotify


def get_next_page_json(json_object, json_list):
    print("Adding a json object...")
    json_list.append(json_object)
    if "next" in json_object["pagination"]["urls"]:
        next_page = json_object["pagination"]["urls"]["next"]
        get_next_page_json(requests.get(next_page, headers=headers).json(), json_list)
    return json_list


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

j = requests.get(collection_uri, headers=headers).json()

json_list = []
collection_list = get_next_page_json(j, json_list)

song_list = []

for i in collection_list:
    for x in i["releases"]:
        artist = x["basic_information"]["artists_sort"]
        for y in x["basic_information"]["tracklist"]:
            track = y["title"]
            song_list.append(Song(artist, track))

s = Spotify()
s.create_playlist()