import requests
import datetime
import pymongo
from urllib.parse import urlencode
from pymongo import MongoClient
import base64

client_id = 'a8731e57f8ef4c83a7623a1f8182dde9'
client_secret = 'a1063792310642e8902a951dc42fe92c'

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_artists_details(self, artists_id):
        artist_details_com = []
        for item in artists_id[:30]:
            endpoint = f"https://api.spotify.com/v1/artists/{item}"
            headers = self.get_resource_header()
            r = requests.get(endpoint, headers=headers)
            if r.status_code not in range(200, 299):
                return {}
            artist_details_com.append(r.json())
        return artist_details_com


    def call_api(self, playlist_id = '37i9dQZF1DXcBWIGoYBM5M'):
        query_params = urlencode({"offset": 0, "country": "US"})  # can change the country code as needed
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_artist_names(self):
        popular_tracks = self.call_api()
        artists = []
        for track in popular_tracks["tracks"]["items"]:
            artists = track["track"]["artists"]
            for artist in artists:
                artist_name = artist["name"]
                artists.append(artist_name)
        return artists

    def get_top_hits(self):
        popular_tracks = self.call_api()
        artists_id = []
        top_hits = []
        for track in popular_tracks["tracks"]["items"]:
            top_hits.append(track)
            artists = track["track"]["artists"]
        #     album_name = track["track"]["album"]["name"]
        #     song_name = track["track"]["name"]
            for artist in artists:
                artist_name = artist["name"]
                if(artist_name != "iñigo quintero"):
                    artist_id = artist["id"]
                    artists_id.append(artist_id)
        return top_hits, artists_id


# Use the modified SpotifyAPI class to get popular tracks
spotify = SpotifyAPI(client_id, client_secret)
top_hits, artists_id = spotify.get_top_hits()
artists_details = spotify.get_artists_details(artists_id)


try:
    client = MongoClient()
    client = MongoClient("localhost", 27017)
    client = MongoClient("mongodb://localhost:27017/")
    print("Connected successfully to Spotify Database!!!")
    db = client["chestnut"]


    collection = db["top_hits"]
    collection.create_index("track",unique=True)
    for item in top_hits:
        try:
            result = collection.insert_one(item)
        except Exception as e:
            print("Ignoring duplicate keys")
    
    print("Inserted spotify top hits successfully")


    collection = db["artists_details"]
    collection.create_index("id",unique=True)
    for item in artists_details:
        try:
            result = collection.insert_one(item)
        except Exception as e:
            print("Ignoring duplicate keys")

    print("Inserted artists details top hits successfully")


except Exception as e:  
    print(f"Could not connect to MongoDB --->> {e}")
