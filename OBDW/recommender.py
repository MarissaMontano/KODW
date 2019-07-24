
#!/usr/bin/env Python3

import database
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


#  Client Keys
CLIENT_ID = "c5e2d53ffcd64af3839e40efbe4a7382"
CLIENT_SECRET = "ec6dfefa3f8e43f8bf3b61da9a77155e"


class Recommender(object):

    def __init__(self):
        self.db = database.Database(r"./OBDW.db")
        self.db.openDatabase()
        auth = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
        token = auth.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)

    # way to interact with database

    # way to grab data from website

    # way to grab data from GUI/API
    def grabUserInfo(self):
        genres = self.spotify.recommendation_genre_seeds()
        print(genres)

    def pullGenres(self, genreList):
        results = self.spotify.recommendations(seed_genres=genreList)
        for track in results['tracks']:
            print (track['name'], '-', track['artists'][0]['name'])


if __name__ == "__main__":
    pass

