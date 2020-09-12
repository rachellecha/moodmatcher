import requests
import datetime
from urllib.parse import urlencode

import base64

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json

# get username from terminal
username = "12171678313"

#Erase cache and prompt for user permission

try:
    token = util.prompt_for_user_token(username)
except:
    #os.remove(".cache-{}".format(username))
    token = token = util.prompt_for_user_token(username, client_id='9d5dc983184743aa992c6a6b81fa44b5', client_secret='b7f6d9fa451e406a98eb541247a63de6', redirect_uri='https://google.com/')

#create spotify object
spotifyObject = spotipy.Spotify(auth=token)

emot = 'anger'
playlist = ''

if emot == 'joy':
    playlist = '37i9dQZF1DXdPec7aLTmlC'
elif emot == 'sorrow':
    playlist = '37i9dQZF1DWSqBruwoIXkA'
elif emot == 'anger':
    playlist = '37i9dQZF1DXcfZ6moR6J0G'
else:
    playlist = '37i9dQZF1DX7HOk71GPfSw'

cover = spotifyObject.playlist_cover_image(playlist)
playlist_cover = cover[0]['url']

playlist_url = spotifyObject.playlist(playlist)

url = playlist_url['external_urls']['spotify']


print(playlist_cover)
print(url)

