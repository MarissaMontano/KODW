
import threading


class SharedState:
    ''' A SharedState is the way we can apply a 'spinlock' approck of threading
        to run both the GUI and Flask app. (https://stackoverflow.com/questions/55432430/how-to-control-a-python-gui-via-http-api)

        _lock: is a threading lock
        _running: is a bool used to see if the app is still running
        _click_count: is an int used to see if someone requested the GUI from Flask
    '''

    def __init__(self):
        self._lock = threading.Lock()
        self._running = True
        self._click_count = 0

    def record_click(self):
        ''' This method is called when the the flask app requests the GUI and all it does
            is increases the _click_count.

            Input: None
            Output: None
        '''
        with self._lock:
            self._click_count += 1

    def clicked(self):
        ''' This method is used to verify we got a request from the Flask app, so
            the GUI can be displayed

            Input: None
            Output: True if _click_count is non-zero, False if otherwise
        '''
        if self._click_count > 0:
            self._click_count -= 1
            return True
        return False

    def stop(self):
        ''' This method is used to kill the spinklock threading loop
            * don't use this anymore because im using a daemon thread

            Input: None
            Output: None
        '''
        # called from either side to stop running
        with self._lock:
            self._running = False
