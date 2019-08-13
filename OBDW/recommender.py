
#!/usr/bin/env Python3

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import time
import threading
from multiprocessing.pool import ThreadPool
import configparser
import pandas as pd
import random
import logging
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from GUI.qtDriver import main as mainGUI
from webFlask import app
from sharedState import SharedState
import database

DIR = os.path.dirname(os.path.abspath(__file__))
CFG_FILE_PATH = os.path.join(DIR, 'OBDW_config.cfg')

class Recommender(object):

    def __init__(self):
        # open config files
        config = configparser.ConfigParser()
        config.read(CFG_FILE_PATH)
        self.flask_cfg = config['flask']
        db_cfg = config['database']
        log_cfg = config['logging']
        self.rec_cfg = config['recommendations']
        self.class_cfg = config['classifier']
        spotify_cfg = config['spotify']

        # open database
        connectStr = os.path.join(DIR, db_cfg['Connection_str'])
        self.db = database.Database(connectStr, db_cfg['Check_thread'])
        self.db.openDatabase()

        # start instance of spotify api
        auth = SpotifyClientCredentials(
            client_id=spotify_cfg['Client_id'],
            client_secret=spotify_cfg['Client_key'])
        token = auth.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)

        # set default classifier
        self.classifier = GradientBoostingClassifier(
            n_estimators=int(self.class_cfg['N_estimators']), learning_rate=float(self.class_cfg['Learning_rate']), max_depth=int(self.class_cfg['Max_depth']), random_state=int(self.class_cfg['Random_state']))

        # Set logging
        logging.basicConfig(filename=os.path.join(DIR, log_cfg['Path']),
                            filemode=log_cfg['Filemode'], format=log_cfg['Format'], level=log_cfg['Level'])
        self.logger = logging.getLogger(__name__)
    

    def getRandomSongs(self, uid):
        ''' This method is used to get a new list of recommendations based on previous liked recomendation

            Input:  user ID
            Output: list of songs
        '''
        # get what genres the user likes
        genreList = self.db.getUserGenres(uid)

        # if they dont have any genre data just recommend new releases
        if len(genreList) == 0:
            results = self.spotify.recommendations(
                seed_genres=['new-release'], limit=int(self.rec_cfg['New_songs']))
        else:
            # can only pass in 5 genres, so need to randomly select some....
            if len(genreList) > 5:
                genreList = random.sample(genreList, 5)

            results = self.spotify.recommendations(
                seed_genres=genreList, limit=int(self.rec_cfg['New_songs']))

        newSongs = []
        for track in results['tracks']:
            newSongs.append([track['id'], track['name'],
                             track['artists'][0]['name'], track['preview_url']])

        # update song database with new music
        self.updateSongData(newSongs)

        # return a list of new song ids
        return newSongs

    def getRandomPredict(self, tracksList):
        ''' This method is used to get a new list of recommendations based on previous 5 star tracks

            Input:  songs (list of song ids)
            Output: cleanData (pandas dataframe that holds tempo, key, mode, etc..)
        '''

        # can only pass in 5 tracks, so need to randomly select some....
        if len(tracksList) > 5:
            tracksList = random.sample(tracksList, 5)

        results = self.spotify.recommendations(
            seed_tracks=tracksList, limit=int(self.rec_cfg['New_songs']))

        newSongs = []
        for track in results['tracks']:
            newSongs.append([track['id'], track['name'],
                             track['artists'][0]['name'], track['preview_url']])

        # update song database with new music
        self.updateSongData(newSongs)
        self.db.commitWork()

        cleanData = self.db.getRandomPredict(newSongs)
        return cleanData

    def updateGenres(self, uid, genreList):
        ''' This method updates what genres are associated with a user

            Input:  user ID
                    list of genres
            Output: None
        '''
        self.db.updateUserGenres(uid, genreList)
        self.db.commitWork()

    def setClassifier(self, classStr):
        ''' This method ....

            Input:  classStr (str)
            Output: None
        '''
        if classStr == "K-Nearest Neighbors":
            self.classifier = KNeighborsClassifier(
                int(self.class_cfg['Neighbors']))
        elif classStr == "RBF SVM":
            self.classifier = SVC(gamma=float(
                self.class_cfg['Gamma']), C=float(self.class_cfg['C']))
        else:
            self.classifier = GradientBoostingClassifier(
                n_estimators=int(self.class_cfg['N_estimators']), learning_rate=float(self.class_cfg['Learning_rate']), max_depth=int(self.class_cfg['Max_depth']), random_state=int(self.class_cfg['Random_state']))

    def updateCache(self, action):
        if action:
            self.logger.debug('starting to update cache')
            # update databse with #New_Songs new songs from every genre
            newSongs = []
            genreList = self.spotify.recommendation_genre_seeds()
            for genre in genreList['genres']:
                results = self.spotify.recommendations(
                    seed_genres=[genre], limit=int(self.rec_cfg['New_songs']), country='US')
                for track in results['tracks']:
                    newSongs.append(
                        [track['id'], track['name'], track['artists'][0]['name'], track['preview_url']])
            # update song database with new music
            self.updateSongData(newSongs)
        else:
            pass
        self.logger.debug('Done update cache')

    def updateSongData(self, newSongs):
        ''' This method updates the Song table with new music data based on songIDs

            Input:  song IDs, names, artists, and  song URLs (4D array)
            Output: None
        '''
        # Get music data related to the song ids
        musicData = []
        songIds = [songs[0] for songs in newSongs]

        # can only get 50 songs at a time!
        for ids in range(0, len(songIds), 50):
            tracks = (self.spotify.audio_features(songIds[ids:ids+50]))
            more_features = newSongs[ids:ids+50]
            for idx, song in enumerate(tracks):
                if song is None:
                    pass
                else:
                    musicData.append([song['id'], song['key'], song['mode'], song['acousticness'], song['danceability'], song['energy'], song['instrumentalness'], song['liveness'],
                                      song['loudness'], song['speechiness'], song['valence'], song['tempo'], more_features[idx][1], more_features[idx][2], more_features[idx][3]])
        # add music to datbase
        self.db.updateSongTable(musicData)
        self.db.commitWork()

    def calculateRecommendataion(self, uid):
        ''' This method updates the web app with new recommendations for a user

            Input:  User ID (int), type of classifier(string)
            Output: None
        '''
        self.logger.debug('Starting to collect new recommendations')
        # get songs their raitings, and train the recommender
        userData = self.db.getUsersSongData(uid)

        # get list of over 4 stared tracks:
        userTracks = self.db.getUserTracks(uid)
        # if there is no user data or they have rated less than 5, >4 star songs, recommend 10 random songs based off of genres
        if userData is None or len(userTracks) < int(self.rec_cfg['Min_data_points']):
            # get some random (semi-filterd) songs to feed in recommender
            songIds = [songs[0] for songs in self.getRandomSongs(uid)]
            recommendations = self.db.formatRecommendations(
                songIds[:int(self.rec_cfg['N_recommendations'])], uid)
        else:
            predictData = self.getRandomPredict(userTracks)

            features = ['Key', 'Mode', 'Acousticness', 'Danceability', 'Energy',
                        'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Valence', 'Tempo']
            x_data = userData[features]
            y_data = userData['Rating']

            self.classifier.fit(x_data, y_data)
            prediction = self.classifier.predict(predictData[features])
            songsRec = []
            for idx, guess in enumerate(prediction):
                if guess >= int(self.rec_cfg['threshold']):
                    songsRec.append(predictData['ID'][idx])
                if len(songsRec) == int(self.rec_cfg['N_recommendations']):
                    break
            recommendations = self.db.formatRecommendations(songsRec, uid)
        self.logger.debug('Done collecting new recommendations')
        # recommendation is [songName,songArtist SongURL]
        return(recommendations)

    def webserver(self, shared_state):
        ''' This method is used to start the web server and set the configuration
            handeling for the shared state

            Input: sharedState
            Output: None
        '''
        # set config for the shared state to pass messages
        app.config['SHARED'] = shared_state

        # set secret key for sessions
        app.secret_key = os.urandom(int(self.flask_cfg['Secret_key']))
        # run the app
        app.run(host=self.flask_cfg['Host'], port=int(self.flask_cfg['Port']),
                debug=self.flask_cfg['Debug'], use_reloader=False)

    def runApp(self):
        ''' This method is used to run the spinlock threading loop and terminate
            the Flask app gracefully.

            Input: None
            Output: None
        '''
        shared_state = SharedState()
        ui_thread = threading.Thread(
            target=self.webserver, args=(shared_state,))
        # Make the Flask thread daemon so they are automagically killed for us
        ui_thread.setDaemon(True)
        ui_thread.start()
        self.logger.info('App Started, opening...')

        # this is the spinlock threading loop that shows the GUI when prompted from Flask
        try:
            while shared_state._running:
                time.sleep(0.1)
                # if the gui is open....
                if shared_state.clicked():
                    self.logger.info('User requested the GUI')
                    output = mainGUI()
                    if len(output) == 3:
                        # update genres, and recommender
                        uid = shared_state.currentUser
                        if uid is not None:
                            self.logger.info('User updated app prefrences')
                            self.setClassifier(output[1])
                            self.updateGenres(uid, output[0])
                            # update cache
                            self.updateCache(output[2])
                    else:
                        self.logger.info('User canceled GUI')
                        pass
                if shared_state.refresh():
                    self.logger.info(
                        'User requested to refresh list of recommendations')
                    # refresh takes a while, so put in thread
                    pool = ThreadPool(1)
                    uid = shared_state.currentUser
                    shared_state.recommenList = pool.map(
                        self.calculateRecommendataion, [uid])[0]
                    pool.close()
                    pool.join()
            ui_thread.join()

        # gracefully terminates when Ctrl-c is hit
        except KeyboardInterrupt:
            self.logger.info('App stopped, exiting...')
            self.db.closeDatabase()
            exit(0)


if __name__ == '__main__':
    engine = Recommender()

    #engine.db.deleteUser(2, "world")
    # engine.db.commitWork()
    # engine.db.closeDatabase()

    engine.runApp()
