import threading
import time
import os
from GUI.Qt_hello_world import main as mainGUI

from webFlask import app
PORT = 3000

class SharedState:
    def __init__(self):
        self._lock = threading.Lock()
        self._running = True
        self._click_count = 0

    def record_click(self):
        # this gets called from the Flask thread to record a click
        with self._lock:
            self._click_count += 1
            
    def clicked(self):
        # this gets called from the GUI thread to 'get' a click
        with self._lock:
            if self._click_count > 0:
                self._click_count -= 1
                return True
            return False
    def stop(self):
        # called from either side to stop running
        with self._lock:
            self._running = False

def webserver(shared_state):
    app.config['SHARED'] = shared_state
    # It isn't safe to use the reloader in a thread
    app.secret_key = os.urandom(16)
    app.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)


def main():
    shared_state = SharedState()
    ui_thread = threading.Thread(target=webserver, args=(shared_state,))
    ui_thread.start()

    while shared_state._running:
        time.sleep(0.1)
        if shared_state.clicked():
            mainGUI()
    ui_thread.join()

if __name__ == '__main__':
    main()