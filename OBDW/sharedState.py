
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
        self._refresh_count = 0
        self._login_count = 0
        self._create_count = 0
        self._delete_count = 0
        self._rating_count = 0
        self.currentUser = None
        self.recommenList = []
        self.loggin_in = []
        self.create_user = []
        self.delete_user = []
        self.user_ratings = []
        self.loading = False

    def record_click(self, uid):
        ''' This method is called when the the flask app requests the GUI and all it does
            is increases the _click_count.

            Input: userID
            Output: None
        '''
        self.currentUser = uid
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

    def record_refresh(self, uid):
        ''' This method is called when the the flask app wants to refreshe

            Input: userID
            Output: None
        '''
        self.currentUser = uid
        with self._lock:
            self._refresh_count += 1

    def refresh(self):
        ''' This method is used to send a signal to physically display recomendations

            Input: None
            Output: True if _refresh_count is non-zero, False if otherwise
        '''
        if self._refresh_count > 0:
            self._refresh_count -= 1
            return True
        return False

    def record_login(self, username, password):
        ''' This method is called when the the flask app wants someone to login user

            Input:  username (str)
                    password (str)
            Output: None
        '''
        self.loggin_in = [username, password]
        with self._lock:
            self._login_count += 1

    def login(self):
        ''' This method is used to send a signal to physically log someing in 
            Input: None
            Output: True if _login_count is non-zero, False if otherwise
        '''
        if self._login_count > 0:
            self._login_count -= 1
            return True
        return False

    def record_create(self, username, password, password2):
        ''' This method is called when the the flask app wants someone to create user

            Input:  username (str)
                    password (str)
                    password2 (str)
            Output: None
        '''
        self.create_user = [username, password, password2]
        with self._lock:
            self._create_count += 1

    def create(self):
        ''' This method is used to send a signal to physically create the user
            Input: None
            Output: True if _create_count is non-zero, False if otherwise
        '''
        if self._create_count > 0:
            self._create_count -= 1
            return True
        return False

    def record_delete(self, uid, password):
        ''' This method is called when the the flask app wants someone to delete user

            Input:  uid (int)
                    password (str)
            Output: None
        '''
        self.delete_user = [uid, password]
        with self._lock:
            self._delete_count += 1

    def delete(self):
        ''' This method is used to send a signal to physically delete the user
            Input: None
            Output: True if _delete_count is non-zero, False if otherwise
        '''
        if self._delete_count > 0:
            self._delete_count -= 1
            return True
        return False

    def record_user_rating(self, ratedSongs):
        ''' This method is called when the the flask app wants someone to delete user

            Input:  uid (int)
                    password (str)
            Output: None
        '''
        self.user_ratings = ratedSongs
        with self._lock:
            self._rating_count += 1

    def rate_songs(self):
        ''' This method is used to send a signal to physically delete the user
            Input: None
            Output: True if _delete_count is non-zero, False if otherwise
        '''
        if self._rating_count > 0:
            self._rating_count -= 1
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
