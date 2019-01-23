import librosa
from enum import Enum, auto
from mixlist import song

class Analyzer:
    class AnalyzerEnums(Enum):
        TEMPO = auto()
        KEY = auto()
        BEATS = auto()

    @staticmethod
    def analyze(song, *args):
        """
        Analyze the provided song and store it in the analysis attribute of the Song object

        :param song: the song to analyze
        :param *args: the attributes of the song to analyze, need to be defined enums, if none are provided then all attributes are analyzed
        :raises ValueError: if one of the attributes requested does not exist
        """
        switch = {
            Analyzer.AnalyzerEnums.TEMPO : Analyzer._analyze_tempo,
            Analyzer.AnalyzerEnums.KEY : Analyzer._analyze_key,
            Analyzer.AnalyzerEnums.BEATS : Analyzer._analyze_beats
        }

        song.analysis = {}
        if len(args) == 0:
            for attr in list(Analyzer.AnalyzerEnums):
                switch[attr](song)
        else:
            for attr in args:
                if attr not in switch:
                    raise ValueError("%s not a defined attribute of a song" % attr)
                else:
                    switch[attr](song)

    @staticmethod
    def _analyze_tempo(song):
        print("Analyzing tempo for %s" % song.get_name())
        song.analysis[Analyzer.AnalyzerEnums.TEMPO] = librosa.beat.tempo(song.samples, sr=song.sample_rate)

    @staticmethod
    def _analyze_beats(song):
        print("Analyzing beats for %s" % song.get_name())
        tempo, beats = librosa.beat.beat_track(song.samples, sr=song.sample_rate, units='time')
        song.analysis[Analyzer.AnalyzerEnums.TEMPO] = tempo 
        song.analysis[Analyzer.AnalyzerEnums.BEATS] = beats 
    
    @staticmethod
    def _analyze_key(song):
        pass