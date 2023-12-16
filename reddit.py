from spotifyUtil import get_artist_names
import requests
import pymongo

# def find_artists_in_music(db):
#     collection = db.rMusic
#     result = collection.find({
#         "post": {
#             "$regex": "TaylorSwift*",
#             "$options": "i"
#         }
#     })
#     for document in result:
#         print(document)

def call_spotify(headers, db):
    try:
        #Subreddit r/spotify
        
        link = "https://oauth.reddit.com/r/spotify/"
        res = requests.get(link, headers=headers)
        res.json()

        collection = db.rSpotify
        collection.create_index("post",unique=True)
        


        post_list = res.json()['data']['children']
        i = 1
        i = len(post_list)
        if len(post_list) > 0:
            for post in post_list:
                try:
                    collection.insert_one({"id":i, "post":post['data']['title'], "number_of_comments":post['data']['num_comments']})
                except Exception as e:
                    if "E11000 duplicate key error" in str(e):
                        # If a duplicate key error occurs, update the existing document
                        query = {"post": post['data']['title']}
                        new_data = {
                            "$set": {
                                "number_of_comments": post['data']['num_comments']  # Update the number_of_comments field with the new value
                            }
                        }
                        collection.update_one(query, new_data)
                i += 1
    except Exception as e:
        print(f" Exception in call_spotify - {e}")
        


def call_popheads(headers, db):
    try:

        # #Subreddit r/popheads
        link = f"https://oauth.reddit.com/r/popheads/"

        collection = db.rPopheads 
        collection.create_index("post", unique=True)


        popheads_data = requests.get(link, headers=headers).json()
        popheads_post_list = popheads_data['data']['children']
        i = 1  

        if len(popheads_post_list) > 0:
            for post in popheads_post_list:
                try:
                    collection.insert_one({"id": i, "post": post['data']['title'], "number_of_comments": post['data']['num_comments']})
                except Exception as e:
                    if "E11000 duplicate key error" in str(e):
                        # If a duplicate key error occurs, update the existing document
                        query = {"post": post['data']['title']}
                        new_data = {
                            "$set": {
                                "number_of_comments": post['data']['num_comments']  # Update the number_of_comments field with the new value
                            }
                        }
                        collection.update_one(query, new_data)
                i += 1
    except Exception as e:
        print(f" Exception in call_popheads - {e}")


def call_music(headers, db):
    try:
        # #Subreddit r/Music
        link = f"https://oauth.reddit.com/r/Music/"

        collection = db.rMusic
        collection.create_index("post", unique=True)

        music_data = requests.get(link, headers=headers).json()
        music_post_list = music_data['data']['children']
        i = 1

        if len(music_post_list) > 0:
            for post in music_post_list:
                try:
                    collection.insert_one({"id":i, "post":post['data']['title'], "number_of_comments":post['data']['num_comments']})
                except Exception as e:
                    if "E11000 duplicate key error" in str(e):
                        # If a duplicate key error occurs, update the existing document
                        query = {"post": post['data']['title']}
                        new_data = {
                            "$set": {
                                "number_of_comments": post['data']['num_comments']  # Update the number_of_comments field with the new value
                            }
                        }
                        collection.update_one(query, new_data)
                i += 1
    except Exception as e:
        print(f" Exception in call_music - {e}")


def call_reddit_api():
    CLIENT_ID = 'wDwbMsIW6a_9e4PXO4AKnw'
    SECRET_KEY = 'AMRG2tLpvjR80IAU7iOAUmW_NgjE0g'

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
        'grant_type': 'password',
        'username': 'SocialMediaFreaks515',
        'password': 'Khaleesi@37'
    }

    # headers = {'User-Agent': 'Project1'}
    headers = {'User-Agent': 'Disha Shetty/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    #print(res.json())
    TOKEN = res.json()['access_token']
    # headers = {*headers, *{'Authorization': f'bearer {TOKEN}'}}
    headers = {**headers, 'Authorization': f'Bearer {TOKEN}'}

    try:
        conn = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        print("Connected successfully to Reddit Database!!!")
    except:
        print("Could not connect to MongoDB")
    
    try:
        db = conn.chestnut
        # find_artists_in_music(db)
        call_spotify(headers, db)

        call_popheads(headers, db)

        call_music(headers, db)

        print(" Updated database of spotify, popheads and music ")

        
        # Filtering out the useful data with top trending artists

        client_id = 'a8731e57f8ef4c83a7623a1f8182dde9'
        client_secret = 'a1063792310642e8902a951dc42fe92c'
        artist_names_of_top_hits = get_artist_names(client_id, client_secret)

        artist_names = [name for name in artist_names_of_top_hits if name != "iñigo quintero"]
        artist_names_20 = artist_names[:30]
        for name in artist_names_20:
        
            name_edited = name.replace(' ', '').replace(".", "")

            collection = db.artists_posts
            collection.create_index("post",unique=True)
        
            music_data = requests.get(f"https://oauth.reddit.com/r/{name_edited}/", headers=headers).json()

            if (music_data.get("error") != 404):
                if(music_data.get("error") != 403):
                    music_post_list = music_data['data']['children']

                    if len(music_post_list) > 0:
                        for post in music_post_list:
                            try:
                                collection.insert_one({"post": post['data']['title'], "number_of_comments": post['data']['num_comments'], "artist": name_edited})
                            except Exception as e:
                                if "E11000 duplicate key error" in str(e):
                                    query = {"post": post['data']['title']}
                                    new_data = {
                                        "$set": {
                                            "number_of_comments": post['data']['num_comments']  # Update the number_of_comments field with the new value
                                        }
                                    }
                                    collection.update_one(query, new_data) 
        print('Updated artist data successfully')

    except Exception as e:
        print(f"Error - {e}")

# call_reddit_api()
