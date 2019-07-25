
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

    # way to interact with database

    # way to grab data from website

    # way to grab data from GUI/API

    def pullGenres(self, genreList):
        results = self.spotify.recommendations(seed_genres=genreList)
        for track in results['tracks']:
            print (track['name'], '-', track['artists'][0]['name'])

    def webserver(self, shared_state):
        ''' This method is used to start the web server and set the configuration 
            handeling for the shared state

            Input: sharedState
            Output: None
        '''
        # set config for the shared state to pass messages
        app.config['SHARED'] = shared_state
        
        app.secret_key = os.urandom(16)
        # run the app
        app.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)


    def runApp(self):
        ''' This method is used to run the spinlock threading loop and terminate
            the Flask app gracefully.

            Input: None
            Output: None
        '''
        # thread the Flask app
        shared_state = SharedState()
        ui_thread = threading.Thread(target=self.webserver, args=(shared_state,))
        # Make the Flask thread daemon so they are automagically killed for us
        ui_thread.setDaemon(True)
        ui_thread.start()

        # this is the spinlock threading loop that shows the GUI when prompted from Flask
        try:
            while shared_state._running:
                time.sleep(0.1)
                if shared_state.clicked():
                    genre, classi = mainGUI()
                    print(genre, classi)
            # TODO: understand what thread.join() does and how to properly kill the thread
            ui_thread.join()

        # gracefully terminates when Ctrl-c is hit
        except KeyboardInterrupt:
            # print(ui_thread.isAlive())
            print("exiting")
            exit(0)


if __name__ == '__main__':
    engine = Recommender()
    engine.runApp()



