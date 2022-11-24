from flask import Flask, render_template
import base64
import requests
import datetime
from urllib.parse import urlencode
import json
import spotipy
import requests
import os
import urllib.request
import random

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/work")
def work():
	return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("about.html")

@app.route('/spotify_get_current_track')
def spotify_get_current_track():
	client_id = "f9b92a146a3b4a4b90c558b23c82b918"
	client_secret = "03c964ed7eab4e739f4ce68c133b8c66"
	refresh_token = "AQAeEUbLzSsG6YgwO32hxxKdQtVDHWgcJX9zDVnsJHwf-lBxnWn3l_JI1ObdTfQFrq7KrFnjffvY3hSvzpdWwwG74Wkvv12sU1IJt-PpPV3nQ2DTcyzxDYbTz1WPjRTHpsY"
	refresh_token_url = "https://accounts.spotify.com/api/token"
	refresh_token_body = {
		'grant_type':'refresh_token',
		'refresh_token':refresh_token
	}
	client_creds = f"{client_id}:{client_secret}"
	client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
	refresh_token_header = {
		'Authorization':f"Basic {client_creds_b64}"
	}
	r = requests.post(refresh_token_url,data=refresh_token_body,headers=refresh_token_header)
	access_token = r.json()['access_token']

	currently_playing_url = "https://api.spotify.com/v1/me/player/currently-playing"
	currently_playing_headers = {
		'Authorization': f"Bearer {access_token}",
		'Content-Type': 'application/json'
	}
	r = requests.get(currently_playing_url,headers = currently_playing_headers)
	print(f"{r.json()['item']['name']} by {r.json()['item']['artists'][0]['name']}")
	image_url = r.json()['item']['album']['images'][0]['url']
	img_data = requests.get(image_url).content
	mydir = './static/assets/img/cache'
	filelist = [ f for f in os.listdir(mydir) if f.endswith(".jpg") ]
	for f in filelist:
		os.remove(os.path.join(mydir, f))
	r1 = random.randint(0, 10) 
	with open('static/assets/img/cache/current_track_'+str(r1)+'.jpg', 'wb') as handler:
		handler.write(img_data)
	response = {
		'track_image_filename':'static/assets/img/cache/current_track_'+str(r1)+'.jpg',
		'display_string': f"{r.json()['item']['name']} by {r.json()['item']['artists'][0]['name']}"
	}
	return (response)

if __name__ == "__main__":
	app.run(debug=True)
