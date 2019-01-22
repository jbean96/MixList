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
    
    def analyze(self, *args):
        """
        Analyze the provided song and stores the analyzed attributes in self.analysis, if the song has not been loaded yet, it loads it as well

        :param song: the song to analyze
        :param *args: the attributes of the song to analyze, need to be defined enums, if none are provided then all attributes are analyzed
        """
        if not self.is_loaded():
            self.load()
        
        print("Analyzing: %s" % self.get_name())
        self.analysis = Analyzer.analyze(self, *args)

    def is_analyzed(self, attr=None):
        if attr is None:
            return self.analysis is not None
        else:
            return self.analysis is not None and attr in self.analysis

    def get_tempo(self):
        if not self.is_analyzed(Analyzer.TEMPO):
            self.analyze(Analyzer.TEMPO)
        
        return self.analysis[Analyzer.TEMPO]

    @staticmethod
    def load_song(song):
        """
        Static method to load a song, needed to do multiprocess loading of songs in util.Methods.load_songs

        :param song: the song to load
        """
        song.load()