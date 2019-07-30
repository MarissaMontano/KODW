
#!/usr/bin/env Python3

import database
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import time
import threading
from GUI.Qt_hello_world import main as mainGUI
from webFlask import app
from sharedState import SharedState
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC 

#  Client Keys
CLIENT_ID = "c5e2d53ffcd64af3839e40efbe4a7382"
CLIENT_SECRET = "ec6dfefa3f8e43f8bf3b61da9a77155e"
PORT = 3000


class Recommender(object):

    def __init__(self):
        self.db = database.Database(r"./OBDW.db")
        self.db.openDatabase()
        auth = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
        token = auth.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)
        self.classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=.1, max_depth=1, random_state=0)

    # way to plot recomendations to web
            # Make sure it takes in recommendation string

    # way to grab data from website

    # way to grab data from GUI/API

    def grabRandomSongs(self, uid):
        ''' This method is used grab a new list of recommendations based on previous liked recomendation

            Input:  user ID
            Output: list of songs
        '''
        # grab what genres the user likes
        db = database.Database(r"./OBDW.db")
        db.openDatabase()
        genreList = db.grabUserGenres(uid)
        db.closeDatabase()

        # if they dont have any genre data just recommend new releases
        if len(genreList) == 0:
            results = self.spotify.recommendations(
                seed_genres=['new-release'], limit=25)
        else:
            results = self.spotify.recommendations(
                seed_genres=genreList, limit=25)
        newSongs = []
        for track in results['tracks']:
            newSongs.append([track['id'], track['name'], track['artists'][0]['name'], track['preview_url']])

        # update song database with new music
        self.updateSongData(newSongs)

        # return a list of new song ids
        return newSongs

    def updateGenres(self, uid, genreList):
        ''' This method updates what genres are associated with a user

            Input:  user ID
                    list of genres
            Output: None
        '''
        db = database.Database(r"./OBDW.db")
        db.openDatabase()
        db.updateUserGenres(uid, genreList)
        db.closeDatabase()

    def setClassifier(self, classStr):
        if classStr == "K-Nearest Neighbors":
            self.classifier = KNeighborsClassifier(3)
        elif classStr == "RBF SVM":
            self.classifier = SVC(gamma=0.1, C=1.0)
        else:
            self.classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=.1, max_depth=1, random_state=0)


    def updateSongData(self, newSongs):
        ''' This method updates the Song table with new music data based on songIDs

            Input:  song IDs and song URLs (2D array)
            Output: None
        '''
        # Grab music data related to the song ids
        musicData = []
        songIds = [songs[0] for songs in newSongs]
        features = self.spotify.audio_features(songIds)
        for idx, song in enumerate(features):
            musicData.append([song['id'], song['key'], song['mode'], song['acousticness'], song['danceability'], song['energy'], song['instrumentalness'], song['liveness'], song['loudness'], song['speechiness'], song['valence'], song['tempo'], newSongs[idx][1], newSongs[idx][2], newSongs[idx][3]])

        # add music to datbase
        db = database.Database(r"./OBDW.db")
        db.openDatabase()
        db.updateSongTable(musicData)
        db.closeDatabase()


    def calculateRecommendataion(self, uid):
        ''' This method updates the web app with new recommendations for a user

            Input:  User ID (int), type of classifier(string)
            Output: None
        '''
        # grab songs their raitings, and train the recommender
        db = database.Database(r"./OBDW.db")
        db.openDatabase()
        userData = db.getUsersSongData(uid)

        # grab some random (semi-filterd) songs to feed in recommender
        songIds = [songs[0] for songs in self.grabRandomSongs(uid)]
        # if there is no user data, recommend 10 random songs based off of genres
        if userData == []:
            #################################only doing this one################
            recommendations = db.formatRecommendations(songIds[:10])
        else:
            predictData = db.cleanPredict(songIds)

            features = ['Key', 'Mode', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Valence', 'Tempo']
            x_data = userData[features]
            y_data = userData['Rating']
            self.classifier.fit(x_data, y_data)
            prediction = self.classifier.predict(predictData)
            songsRec = []
            for idx, guess in enumerate(prediction):
                #for non binary, if binary: if guess
                if guess >= 4:
                    songsRec.append(songIds[idx]) 
                if len(songsRec) == 10:
                    break
            recommendations = db.formatRecommendations(songsRec)           
        #recommendation is [songName,songArtist SongURL]
        print(recommendations)


    def webserver(self, shared_state):
        ''' This method is used to start the web server and set the configuration
            handeling for the shared state

            Input: sharedState
            Output: None
        '''
        # set config for the shared state to pass messages
        app.config['SHARED']= shared_state

        app.secret_key= os.urandom(16)
        # run the app
        app.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)


    def runApp(self):
        ''' This method is used to run the spinlock threading loop and terminate
            the Flask app gracefully.

            Input: None
            Output: None
        '''
        shared_state= SharedState()
        ui_thread= threading.Thread(target=self.webserver, args=(shared_state,))
        # Make the Flask thread daemon so they are automagically killed for us
        ui_thread.setDaemon(True)
        ui_thread.start()

        # this is the spinlock threading loop that shows the GUI when prompted from Flask
        try:
            while shared_state._running:
                time.sleep(0.1)
                if shared_state.clicked():
                    output = mainGUI()
                    if len(output) == 2:
                        # update genres, and recommender
                        uid = shared_state.currentUser
                        if uid is not None:
                            self.setClassifier(output[1])
                            self.updateGenres(uid, output[0])
                            self.calculateRecommendataion(uid)
                    else:
                        pass
            # TODO: understand what thread.join() does and how to properly kill the thread
            ui_thread.join()

        # gracefully terminates when Ctrl-c is hit
        except KeyboardInterrupt:
            # print(ui_thread.isAlive())
            print("exiting")
            exit(0)


if __name__ == '__main__':
    engine= Recommender()
    engine.runApp()
