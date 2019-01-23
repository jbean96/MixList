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
        self.analysis = {}
    
    def get_name(self):
        return os.path.basename(self.path)

    def get_duration(self):
        if not self.is_loaded():
            self.load()
        return librosa.get_duration(self.samples, self.sample_rate)

    def load(self):
        if self.is_loaded():
            print("Song %s already loaded..." % self.get_name())
            return
        
        print("Loading: %s" % self.get_name())
        self.samples, self.sample_rate = librosa.load(self.path, res_type=util.Globals.resample_method)

    def is_loaded(self):
        return self.samples is not None and self.sample_rate is not None
    
    def output(self, path):
        if not self.is_loaded():
            self.load()
        
        print("Outputting song to file: %s" % path)
        librosa.output.write_wav(path, y=self.samples, sr=self.sample_rate)
    
    def analyze(self, *args):
        """
        Analyze the provided song and stores the analyzed attributes in self.analysis, if the song has not been loaded yet, it loads it as well

        :param song: the song to analyze
        :param *args: the attributes of the song to analyze, need to be defined enums, if none are provided then all attributes are analyzed
        """
        if not self.is_loaded():
            self.load()
        
        Analyzer.analyze(self, *args)

    def is_analyzed(self, attr):
        return attr in self.analysis

    def get_tempo(self):
        if not self.is_analyzed(Analyzer.AnalyzerEnums.TEMPO):
            self.analyze(Analyzer.AnalyzerEnums.TEMPO)
        
        return self.analysis[Analyzer.AnalyzerEnums.TEMPO]
    
    def get_beats(self):
        if not self.is_analyzed(Analyzer.AnalyzerEnums.BEATS):
            self.analyze(Analyzer.AnalyzerEnums.BEATS)
        
        return self.analysis[Analyzer.AnalyzerEnums.BEATS]

    ### DOES NOT WORK RIGHT NOW THE SONG OBJECT IS COPIED INTO ANOTHER PROCESS AND THUS WE LOSE THE LOADED DATA ###
    @staticmethod
    def load_song(song):
        """
        Static method to load a song, needed to do multiprocess loading of songs in util.Methods.load_songs

        :param song: the song to load
        """
        song.load()