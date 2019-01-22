import librosa
from mixlist import util

class Song:
    def __init__(self, path):
        # TODO: Potentially use "os" package to get full path to the song
        self.path = path
        self.samples = None
        self.sample_rate = None
        
    def load(self):
        self.samples, self.sample_rate = librosa.load(self.path, res_type=util.Globals.resample_method)

    @staticmethod
    def load_song(song):
        song.load()