from flask import Flask, request, redirect
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("SECRET_ID")
redirect_uri = os.getenv("REDIRECT_URI")
scope = ["user-library-read"]


@app.route("/")
def login():
    print("CLIENT_ID:", client_id)
    print("SECRET_ID:", client_secret)
    print("REDIRECT_URI:", redirect_uri)
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url(
        "https://accounts.spotify.com/authorize"
    )
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    full_url = request.url
    token = oauth.fetch_token(
        "https://accounts.spotify.com/api/token",
        authorization_response=full_url,
        client_secret=client_secret,
    )

    # Save token for reuse
    with open("token.json", "w") as f:
        json.dump(token, f)

    print("✓ Token obtained. You can return to your terminal.")
    return "✅ Spotify authorized! You can now return to the loader."


if __name__ == "__main__":
    app.run(port=8888)
