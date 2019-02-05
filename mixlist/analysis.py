from enum import Enum, auto
from typing import Any

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

    @staticmethod
    def is_feature(feature: 'Feature'):
        return feature in Feature.__members__.values()

class Analysis:
    def __init__(self) -> 'Analysis':
        self._features = {}

    def __str__(self) -> str:
        return str(self._features)
    
    def set_feature(self, feature: Feature, value: Any):
        """
        Sets the specified feature in this analysis object

        @param feature: The Analysis.Feature to set
        @param value: The value to set for the feature
        """
        if not Feature.is_feature(feature):
            raise ValueError("%s is not a valid Analysis.Feature" % str(feature))

        self._features[feature] = value

    def get_feature(self, feature: Feature) -> Feature:
        """
        Gets a specified Analysis.Feature from this Analysis, or None if it isn't an analyzed feature

        @param feature: The Analysis.Feature to return
        @return: The requested Analysis.Feature or None if it isn't in the 
        """
        if not Feature.is_feature(feature):
            raise ValueError("%s is not a valid Analysis.Feature" % str(feature))

        if feature not in self._features:
            return None

        return self._features[feature]