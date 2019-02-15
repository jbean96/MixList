import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

CLIENT_ID = '3f1aa13bb7db466fa6294a27157b3776'
CLIENT_SECRET = '608ad2aef74c494795d6e0d7927de725'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def ratio_comparison(val1: float, val2: float, exp: float=1.0) -> float:
    """
    Computes the ratio comparison of the two values i.e. 1.0 - abs(val2 - val1) / val1, can be
    modified by adding an exponent specified by the exp parameter resulting in the function
    1.0 - (abs(val2 - val1) ** exp) / val1

    @param val1: The value to which your comparing the ratio of difference
    @param val2: The value to compare with
    @param exp: The exponent to raise the numerator to
    @return: The ratio comparison between the two values with a max value of 1.0 and a min value
        of 0.0 (inclusive)
    @raises: ValueError if exp <= 0.0
    """
    if exp <= 0.0:
        raise ValueError("Parameter exp must be > 0.0, specified value is: %f" % exp)

    return 1.0 - (min((abs(val2 - val1) ** exp), val1) / val1 * 1.0)

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
