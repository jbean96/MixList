import librosa
import math
import numpy as np
import pickle
from enum import Enum, auto
from typing import Any, Dict, List, Tuple

from . import keys
from . import util

class Beat:
    class DownBeatAnalysis(Enum):
        NAIVE = auto()
    
    #INDEX_VALUE = 'time' # ['frames', 'samples', 'time']
    INDEX_VALUE = 'samples'
    DOWNBEAT_ANALYSIS = DownBeatAnalysis.NAIVE

    def __init__(self, index: float, is_downbeat: bool=False):
        self.index = index
        self.is_downbeat = is_downbeat

    def get_start_time(self) -> float:
        if Beat.INDEX_VALUE == 'time':
            return self.index
        elif Beat.INDEX_VALUE == 'samples':
            return librosa.samples_to_time(self.index, sr=util.SAMPLE_RATE)
        else:
            raise NotImplementedError("Only samples and time are supported")

    def get_start_sample(self) -> int:
        if Beat.INDEX_VALUE == 'samples':
            return self.index
        elif Beat.INDEX_VALUE == 'time':
            return librosa.time_to_samples(self.index, sr=util.SAMPLE_RATE)
        else:
            raise NotImplementedError("Only samples and time are supported")

    def __str__(self) -> str:
        return "(%f, %s)" % (self.index, "True" if self.is_downbeat else "False")

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.index == other.index and self.is_downbeat == other.is_downbeat

class Feature(Enum):
    BEATS = auto()
    DANCEABILITY = auto()
    DURATION = auto()
    ENERGY = auto()
    KEY = auto()
    LOUDNESS = auto()
    NAME = auto()
    TEMPO = auto()
    TIME_SIGNATURE = auto()
    VALENCE = auto()

FEATURE_TYPES = {
    Feature.BEATS : List[Beat],
    Feature.DANCEABILITY : float,
    Feature.DURATION : float,
    Feature.ENERGY : float,
    Feature.KEY : keys.Camelot,
    Feature.LOUDNESS : float,
    Feature.NAME : str,
    Feature.TEMPO : float,
    Feature.TIME_SIGNATURE : int,
    Feature.VALENCE : float
}

# sanity check
for f in Feature:
    assert f in FEATURE_TYPES

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

    def get_feature(self, feature: Feature) -> Any:
        """
        Gets a specified Analysis.Feature from this Analysis, or None if it isn't an analyzed feature

        @param feature: The Analysis.Feature to return
        @return: The requested Analysis.Feature or None if it isn't in the analysis
        @raise: ValueError if the requested feature is not an Analysis.Feature Enum 
        """
        if not is_feature(feature):
            raise ValueError("%s is not a valid Feature" % str(feature))

        if feature not in self._features:
            if FEATURE_TYPES[feature] == int or FEATURE_TYPES[feature] == float:
                return np.nan
            else:
                return None

        return self._features[feature]
    
def get_closest_beat_to_time(beats: List[Beat], time: float, downbeat: bool=True) -> Beat:
    if downbeat:    
        beats = list(filter(lambda x: x.is_downbeat, beats))
    low = 0
    high = len(beats) - 1
    mid = None
    while (low < high - 1):
        mid = math.floor((low + high) * 1.0 / 2)
        if beats[mid].get_start_time() < time:
            low = mid
        elif beats[mid].get_start_time() > time:
            high = mid
        else: # beats[mid].get_start_time() == time
            return beats[mid]
    closest = (beats[mid], abs(beats[mid].get_start_time() - time))
    if mid - 1 >= 0:
        if closest[1] > abs(beats[mid-1].get_start_time() - time):
            closest = (beats[mid-1], abs(beats[mid-1].get_start_time() - time))
    if mid + 1 < len(beats):
        if closest[1] > abs(beats[mid+1].get_start_time() - time):
            closest = (beats[mid+1], abs(beats[mid+1].get_start_time() - time))
    return closest[0]

def from_file(file_path: str) -> Analysis:
    with open(file_path, "rb") as in_file:
        new_analysis = pickle.loads(in_file.read())
        in_file.close()
        return new_analysis

def analyze_beats(samples: List[float], sample_rate: int) -> Tuple[float, List[Beat]]:
    """
    Analyzes the tempo and the beats of this song and returns them as a tuple

    @return: A Tuple of (tempo, beats)
    """
    tempo, beats = librosa.beat.beat_track(samples, sr=sample_rate, units=Beat.INDEX_VALUE)
    # for now, no downbeats
    beats = list(map(lambda x: Beat(x, False), beats))
    return (tempo, beats)

def analyze_duration(samples: List[float], sample_rate: int) -> float:
    """
    Returns the duration of the song in seconds

    @return: The duration of the song in milliseconds
    """
    duration = librosa.get_duration(samples, sample_rate)
    return duration * 1000 # convert to milliseconds

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