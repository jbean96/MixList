import librosa
from enum import Enum, auto
from mixlist import song

class Analyzer(Enum):
    TEMPO = auto()
    KEY = auto()

    @staticmethod
    def analyze(song, *args):
        """
        Analyze the provided song

        :param song: the song to analyze
        :param *args: the attributes of the song to analyze, need to be defined enums, if none are provided then all attributes are analyzed
        :returns: a dictionary containing the requested analysis attributes (or all if none were specifically requested)
        :raises ValueError: if one of the attributes requested does not exist
        """
        analysis = {}
        if len(args) == 0:
            for attr in Analyzer._switch:
                analysis[attr] = Analyzer._switch[attr](song)
        else:
            for attr in args:
                if attr not in Analyzer._switch:
                    raise ValueError("%s not a defined attribute of a song" % attr)
                else:
                    analysis[attr] = Analyzer._switch[attr](song)

        return analysis

    @staticmethod
    def _analyze_attribute(song, attribute):
        _switch = {
            Analyzer.TEMPO : Analyzer._analyze_tempo,
            Analyzer.KEY : Analyzer._analyze_key
        }
        
        if attribute in _switch:
            return _switch[attribute](song)

    @staticmethod
    def _analyze_tempo(song):
        # TODO: Potentially use onset_envelope (need to lookup first)
        return librosa.beat.tempo(song.samples, sr=song.sample_rate)
    
    @staticmethod
    def _analyze_key(song):
        pass