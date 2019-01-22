import librosa
import os
from mixlist import util
from mixlist.analyzer import Analyzer

class Song:
    def __init__(self, path):
        # TODO: Potentially use "os" package to get full path to the song
        self.path = path
        self.samples = None
        self.sample_rate = None
        self.analysis = None
    
    def get_name(self):
        return os.path.basename(self.path)

    def load(self):
        if self.is_loaded():
            print("Song %s already loaded..." % self.get_name())
            return
        
        print("Loading: %s" % self.get_name())
        self.samples, self.sample_rate = librosa.load(self.path, res_type=util.Globals.resample_method)

    def is_loaded(self):
        return self.samples is not None and self.sample_rate is not None
    
    # TODO: Needs to write sample_rate to the file as well so that both can be loaded faster (not completely necessary)
    def write_to_file(self):
        out_path = self.path[:self.path.rindex(".")]
        out_path = out_path + ".asys"
        print("Writing %s to file %s" % (self.path, out_path))
        if not self.is_loaded():
            self.load()
        
        self.samples.tofile(out_path)
    
    # Analyzes the song, loads/decompresses it if it has not been previously loaded/decompressed
    def analyze(self, *args):
        if not self.is_loaded():
            self.load()
        
        print("Analyzing: %s" % self.get_name())
        self.analysis = Analyzer.analyze(self, *args)

    def is_analyzed(self, attr=None):
        if attr is None:
            return self.analysis is not None
        else:
            return self.analysis is not None and attr in self.analysis

    # Gets the tempo for the song, analyzes the song if it has not been previously analyzed
    def get_tempo(self):
        if not self.is_analyzed(Analyzer.TEMPO):
            self.analyze(Analyzer.TEMPO)
        
        return self.analysis[Analyzer.TEMPO]

    # Needed for batch loading of songs util.Methods.load_songs
    @staticmethod
    def load_song(song):
        song.load()