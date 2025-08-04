from flask import Flask, render_template, session, request, redirect, url_for
import os
import requests
import urllib.parse

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = "https://<your-replit-url>/callback"
SCOPE = "streaming user-read-email user-read-private user-modify-playback-state user-read-playback-state"

@app.route("/")
def index():
    if "access_token" not in session:
        return redirect("/login")
    return render_template("index.html", token=session["access_token"])

@app.route("/login")
def login():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": "true"
    }
    return redirect(f"{auth_url}?{urllib.parse.urlencode(params)}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload)
    token_info = response.json()
    session["access_token"] = token_info["access_token"]
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
