#!/usr/bin/env python3

import os
import time
import threading
from GUI.Qt_hello_world import main as mainGUI
from webFlask import app
from sharedState import SharedState
from recommender import Recommender

PORT = 3000


def webserver(shared_state):
    ''' This function is used to start the web server and set the configuration 
        handeling for the shared state

        Input: sharedState
        Output: None
    '''
    # set config for the shared state to pass messages
    app.config['SHARED'] = shared_state
    
    app.secret_key = os.urandom(16)
    # run the app
    app.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)


def main():
    ''' This function is used to run the spinlock threading loop and terminate
        the Flask app gracefully.

        Input: None
        Output: None
    '''
    #grab Enine
    

    # thread the Flask app
    shared_state = SharedState()
    ui_thread = threading.Thread(target=webserver, args=(shared_state,))
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
    main()
