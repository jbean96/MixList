import librosa
from enum import Enum, auto
from mixlist import song

class Analyzer:
    BEAT_VALUE = 'time' # ['frames', 'samples', 'time']

    class AnalyzerEnums(Enum):
        TEMPO = auto()
        KEY = auto()
        BEATS = auto()
        SECTIONS = auto()

    @staticmethod
    def analyze(song):
        """
        Analyze the provided song and store it in the analysis attribute of the Song object

        @param song: the Song to analyze
        @return: dictionary containing analysis attributes of the song
        """
        analysis = {}

        tempo, beats = Analyzer._analyze_beats(song)
        analysis[TEMPO] = tempo
        analysis[BEATS] = beats

        return analysis

    @staticmethod
    def _analyze_beats(song):
        print("Analyzing beats and tempo for %s" % song.get_name())
        tempo, beats = librosa.beat.beat_track(song.get_samples(), sr=song.Song.SAMPLE_RATE, units=Analyzer.BEAT_VALUE)
        return (tempo, beats)
    
    @staticmethod
    def _analyze_key(song):
        pass
