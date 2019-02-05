import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

CLIENT_ID = '3f1aa13bb7db466fa6294a27157b3776'
CLIENT_SECRET = '608ad2aef74c494795d6e0d7927de725'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def ratio_comparison(val1: float, val2: float, exp: float=1.0) -> float:
    return 1.0 - ((abs(val2 - val1) ** exp) / val1)

class TimerNotStartedException(Exception):
    pass

class TimerAlreadyStartedException(Exception):
    pass

class Timer:
    def __init__(self):
        self.start_time = None
    
    def restart(self):
        self.start_time = datetime.now()

    def start(self):
        if self.start_time is not None:
            raise TimerAlreadyStartedException()

        self.start_time = datetime.now()
        print("Start time: %s" % self.start_time)

    def stop(self):
        if self.start_time is None:
            raise TimerNotStartedException()

        end_time = datetime.now()
        print("End time: %s" % end_time)
        print("Elapsed time: %s" % (end_time - self.start_time))
        self.start_time = None
