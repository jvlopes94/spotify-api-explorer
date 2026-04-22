from flask import Flask, request, redirect
import requests
import threading
import webbrowser

# Spotify API credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8888/callback"
SCOPES = "user-top-read"

app = Flask(__name__)

# Global variable to store the access token
access_token = None


@app.route("/")
def home():
    # Redirect to Spotify's authorization page
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    # Get the authorization code from the query parameters
    auth_code = request.args.get("code")
    if not auth_code:
        return "Authorization failed. Please try again.", 400

    # Exchange the authorization code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        global access_token
        access_token = response.json()["access_token"]
        return "Authorization successful! You can close this tab."
    else:
        return f"Failed to retrieve access token: {response.text}", 400


def get_top_tracks(_time_range: str = "medium_term"):
    if not access_token:
        raise Exception("Access token not available. Please authorize first.")
    if not _time_range:
        _time_range = "medium_term"

    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"time_range": _time_range, "limit": 50}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Failed to fetch top tracks: {response.text}")


def open_browser():
    webbrowser.open("http://localhost:8888")


if __name__ == "__main__":
    # Start the Flask app in a separate thread
    threading.Thread(target=lambda: app.run(port=8888, debug=False)).start()

    # Open the browser to the authorization URL
    open_browser()

    # Wait for user to authorize and retrieve top tracks
    time_range: str = input("Input time range... (short_term, medium_term or long_term)\n")
    try:
        top_tracks = get_top_tracks(time_range)
        print("Your top tracks:")
        for idx, track in enumerate(top_tracks, start=1):
            artists = ", ".join(artist["name"] for artist in track["artists"])
            print(f"{idx}. {track['name']} by {artists}")
    except Exception as e:
        print(f"Error: {e}")
