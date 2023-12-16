import requests
import datetime
from urllib.parse import urlencode
import base64

def get_spotify_data(client_id, client_secret, playlist_id='37i9dQZF1DXcBWIGoYBM5M'):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    token_url = "https://accounts.spotify.com/api/token"

    def get_client_credentials():
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers():
        client_creds_b64 = get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data():
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth():
        token_url = "https://accounts.spotify.com/api/token"
        nonlocal access_token, access_token_expires, access_token_did_expire
        token_url = token_url
        token_data = get_token_data()
        token_headers = get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        access_token = access_token
        access_token_expires = expires
        access_token_did_expire = expires < now

    def get_access_token():
        nonlocal access_token
        token = access_token
        expires = access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            perform_auth()
            return get_access_token()
        elif token is None:
            perform_auth()
            return get_access_token()
        return token

    def get_resource_header():
        access_token = get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    query_params = urlencode({"offset": 0, "country": "US"})  # You can change the country code as needed
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_resource_header()
    r = requests.get(endpoint, headers=headers)
    if r.status_code not in range(200, 299):
        return {}
    return r.json()

def get_artist_names(client_id, client_secret):
    popular_tracks = get_spotify_data(client_id, client_secret)
    artists = []
    for track in popular_tracks["tracks"]["items"]:
        artists_info = track["track"]["artists"]
        for artist in artists_info:
            artist_name = artist["name"]
            artists.append(artist_name)
    return artists
