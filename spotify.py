import requests
import datetime
from urllib.parse import urlencode

import base64

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json

client_id = '9d5dc983184743aa992c6a6b81fa44b5'
client_secret = 'b7f6d9fa451e406a98eb541247a63de6'


# get username from terminal
username = "12171678313"

#12171678313

#Erase cache and prompt for user permission

try:
    token = util.prompt_for_user_token(username)
except:
    #os.remove(".cache-{}".format(username))
    token = token = util.prompt_for_user_token(username, client_id='9d5dc983184743aa992c6a6b81fa44b5', client_secret='b7f6d9fa451e406a98eb541247a63de6', redirect_uri='https://google.com/')

#create spotify object
spotifyObject = spotipy.Spotify(auth=token)

input = input("Song Name? ")

song = spotifyObject.search(input, 1, 0, "track")

album_cover = song['tracks']['items'][0]['album']['images'][0]['url']

print(album_cover)

# print(json.dumps(song, sort_keys = True, indent=4))

trackURI = song["tracks"]["items"][0]["uri"]

searchResults = spotifyObject.audio_features(trackURI)