import librosa
from mixlist import util
from mixlist import analyzer

class Song:
    def __init__(self, path):
        # TODO: Potentially use "os" package to get full path to the song
        self.path = path
        self.samples = None
        self.sample_rate = None
        self.analysis = None
        
    def load(self):
        self.samples, self.sample_rate = librosa.load(self.path, res_type=util.Globals.resample_method)
    
    def analyze(self):
        self.analysis = analyzer.Analyzer.analyze(self)

    # Needed for batch loading of songs util.Methods.load_songs
    @staticmethod
    def load_song(song):
        song.load()