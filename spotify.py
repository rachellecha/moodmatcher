import os
import sys
import spotipy 
import webbrowser
import json
import spotipy.util as util
from json.decoder import JSONDecodeError



# get username from terminal
username = "12171678313"

#Erase cache and prompt for user permission

try:
    token = util.prompt_for_user_token(username)
except:
    #os.remove(".cache-{}".format(username))
    token = token = util.prompt_for_user_token(username, client_id='4c9143d49421423092d55133511a4eaa', client_secret='bf9f6aa8ad074dc8b15ae61ae49b1948', redirect_uri='https://google.com/')

#create spotify object
spotifyObject = spotipy.Spotify(auth=token)

emot = 'joy'
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



