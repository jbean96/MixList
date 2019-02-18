import librosa
import pickle
from enum import Enum, auto
from typing import Any, Dict, List, Tuple

from . import keys

class Feature(Enum):
    BEATS = auto() # TODO: Something with beats to know it's a downbeat?
    DANCEABILITY = auto()
    DURATION = auto()
    ENERGY = auto()
    KEY = auto()
    LOUDNESS = auto()
    NAME = auto()
    TEMPO = auto()
    TIME_SIGNATURE = auto()
    VALENCE = auto()

def is_feature(feature: Feature) -> bool:
    return feature in Feature.__members__.values()

class Analysis:
    def __init__(self):
        self._features = {}

    def __str__(self) -> str:
        return str(self._features)

    def get_unanalyzed_features(self) -> List[Feature]:
        """
        Returns a List of unanalyzed features for this Analysis object

        @return: A List of the Features Enums that aren't currently analyzed for this object
        """
        unanalyzed_features = []
        for f in Feature:
            if f not in self._features:
                unanalyzed_features.append(f)
        return unanalyzed_features

    def is_analyzed(self, feature: Feature) -> bool:
        """
        @return: True if the feature has been analyzed
        """
        return feature in self._features
    
    def set_feature(self, feature: Feature, value: Any):
        """
        Sets the specified feature in this analysis object

        @param feature: The Analysis.Feature to set
        @param value: The value to set for the feature
        @raise: ValueError if the requested feature is not an Analysis.Feature Enum
        """
        if not is_feature(feature):
            raise ValueError("%s is not a valid Feature" % str(feature))

        self._features[feature] = value

    def get_feature(self, feature: Feature) -> Feature:
        """
        Gets a specified Analysis.Feature from this Analysis, or None if it isn't an analyzed feature

        @param feature: The Analysis.Feature to return
        @return: The requested Analysis.Feature or None if it isn't in the analysis
        @raise: ValueError if the requested feature is not an Analysis.Feature Enum 
        """
        if not is_feature(feature):
            raise ValueError("%s is not a valid Feature" % str(feature))

        if feature not in self._features:
            return None

        return self._features[feature]

def from_file(file_path: str) -> Analysis:
    with open(file_path, "rb") as in_file:
        new_analysis = pickle.loads(in_file.read())
        in_file.close()
        return new_analysis

class Beat:
    class DownBeatAnalysis(Enum):
        NAIVE = auto()
    
    #INDEX_VALUE = 'time' # ['frames', 'samples', 'time']
    INDEX_VALUE = 'samples'
    DOWNBEAT_ANALYSIS = DownBeatAnalysis.NAIVE

    def __init__(self, index: float, is_downbeat: bool=False):
        self.index = index
        self.is_downbeat = is_downbeat

def analyze_beats(samples: List[float], sample_rate: int) -> Tuple[float, List[Beat]]:
    """
    Analyzes the tempo and the beats of this song and returns them as a tuple

    @return: A Tuple of (tempo, beats)
    """
    tempo, beats = librosa.beat.beat_track(samples, sr=sample_rate, units=Beat.INDEX_VALUE)
    # Before getting time signature from spotify song, we assume 
    beats = list(map(lambda x: Beat(x, False), beats))
    return (tempo, beats)

def analyze_duration(samples: List[float], sample_rate: int) -> float:
    """
    Returns the duration of the song in seconds

    @return: The duration of the song in milliseconds
    """
    duration = librosa.get_duration(samples, sample_rate)
    return duration * 1000 # want milliseconds

def analyze_key(samples: List[float], sample_rate: int) -> keys.Camelot:
    # TODO: Add our own analysis of key to compare to Spotify API for additional validation
    pass

def annotate_downbeats(beats: List[Beat], time_signature: int) -> List[Beat]:
    new_beats = []
    if Beat.DOWNBEAT_ANALYSIS == Beat.DownBeatAnalysis.NAIVE:
        for (index, beat) in enumerate(beats):
            if index % time_signature == 0:
                new_beat = Beat(beat.index, True)
            else:
                new_beat = Beat(beat.index, False)
            new_beats.append(new_beat)
    else:
        raise NotImplementedError("Only naive downbeat analysis is implemented thus far")
    return new_beats