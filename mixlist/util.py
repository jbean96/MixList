import multiprocessing
import librosa
from datetime import datetime
from mixlist import song

class Globals:
    # Global resampling method to use: ['kaiser_best', 'kaiser_fast', 'scipy']
    resample_method = 'kaiser_best'

class Methods:
    @staticmethod
    def load_songs(songs):
        with multiprocessing.Pool() as p:
            p.map(song.Song.load_song, songs)

class Timer:
    def __init__(self):
        self.start_time = None
    
    def restart(self):
        self.start_time = datetime.now()

    def start(self):
        if self.start_time is not None:
            print("Timer already started")
            return
        self.start_time = datetime.now()
        print("Start time: %s" % self.start_time)

    def stop(self):
        if self.start_time is None:
            print("Timer has not been started yet")
            return
        end_time = datetime.now()
        print("End time: %s" % end_time)
        print("Elapsed time: %s" % (end_time - self.start_time))
        self.start_time = None